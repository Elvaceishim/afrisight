import logging
from datetime import datetime, timezone
from typing import Any

import mlflow
from fastapi import APIRouter

from app.config import get_settings
from app.models.schemas import ExperimentRun
from app.pipeline.tracker import EXPERIMENT_NAME

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/experiments", tags=["experiments"])


def _ms_to_dt(ms: int | None) -> datetime | None:
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


@router.get("", response_model=list[ExperimentRun])
def list_experiments():
    settings = get_settings()
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    try:
        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        if experiment is None:
            return []

        runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
            max_results=100,
            output_format="list",
        )
    except Exception as exc:
        logger.warning("Could not fetch MLflow experiments: %s", exc)
        return []

    results: list[ExperimentRun] = []
    for run in runs:
        info = run.info
        data = run.data
        metrics: dict[str, Any] = data.metrics or {}
        params: dict[str, Any] = data.params or {}

        start_dt = _ms_to_dt(info.start_time)
        end_dt = _ms_to_dt(info.end_time)
        duration = None
        if start_dt and end_dt:
            duration = (end_dt - start_dt).total_seconds()

        results.append(
            ExperimentRun(
                run_id=info.run_id,
                run_name=info.run_name,
                start_time=start_dt,
                duration_seconds=duration,
                article_count=int(metrics.get("article_count", 0)) or None,
                signal_count=int(metrics.get("signal_count", 0)) or None,
                avg_confidence=metrics.get("avg_confidence"),
                prompt_version=params.get("prompt_version"),
                model_name=params.get("model_name"),
                status=info.status,
            )
        )

    return results
