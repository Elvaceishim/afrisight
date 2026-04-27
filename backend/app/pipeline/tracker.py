import json
import os
import tempfile

import mlflow

from app.config import get_settings

EXPERIMENT_NAME = "afrisight-pipeline"


def start_pipeline_run(params: dict) -> str:
    settings = get_settings()
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)
    run = mlflow.start_run()
    mlflow.log_params(params)
    return run.info.run_id


def log_metrics(metrics: dict) -> None:
    mlflow.log_metrics(metrics)


def end_pipeline_run(run_id: str, artifacts: dict) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, prefix="pipeline_summary_"
    ) as f:
        json.dump(artifacts, f, indent=2, default=str)
        tmp_path = f.name

    try:
        mlflow.log_artifact(tmp_path, artifact_path="summary")
    finally:
        os.unlink(tmp_path)
        mlflow.end_run()
