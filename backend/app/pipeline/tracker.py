import json
import logging
import os
import tempfile
import uuid

import mlflow

from app.config import get_settings

logger = logging.getLogger(__name__)

EXPERIMENT_NAME = "afrisight-pipeline"
_mlflow_available = True


def _check_mlflow() -> bool:
    global _mlflow_available
    return _mlflow_available


def start_pipeline_run(params: dict) -> str:
    global _mlflow_available
    settings = get_settings()
    try:
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment(EXPERIMENT_NAME)
        run = mlflow.start_run()
        mlflow.log_params(params)
        _mlflow_available = True
        return run.info.run_id
    except Exception as e:
        logger.warning("MLflow unavailable, skipping tracking: %s", e)
        _mlflow_available = False
        return str(uuid.uuid4())


def log_metrics(metrics: dict) -> None:
    if not _check_mlflow():
        return
    try:
        mlflow.log_metrics(metrics)
    except Exception as e:
        logger.warning("MLflow log_metrics failed: %s", e)


def end_pipeline_run(run_id: str, artifacts: dict) -> None:
    if not _check_mlflow():
        return
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, prefix="pipeline_summary_"
    ) as f:
        json.dump(artifacts, f, indent=2, default=str)
        tmp_path = f.name
    try:
        mlflow.log_artifact(tmp_path, artifact_path="summary")
    except Exception as e:
        logger.warning("MLflow log_artifact failed: %s", e)
    finally:
        os.unlink(tmp_path)
        try:
            mlflow.end_run()
        except Exception:
            pass
