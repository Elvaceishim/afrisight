import logging
import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.database import get_supabase, SIGNALS_TABLE, PIPELINE_RUNS_TABLE
from app.models.schemas import PipelineRunResult, PipelineStatus
from app.pipeline.chain import analyze_article
from app.pipeline.classifier import classify_article
from app.pipeline.ingest import fetch_articles
from app.pipeline.tracker import end_pipeline_run, log_metrics, start_pipeline_run
from app.utils.helpers import clean_text

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/run", response_model=PipelineRunResult)
def run_pipeline():
    run_id = str(uuid.uuid4())
    start_ts = time.time()

    mlflow_run_id = start_pipeline_run(
        {
            "run_id": run_id,
            "model_name": "claude-sonnet-4-20250514",
            "prompt_version": "v1",
        }
    )

    try:
        articles = fetch_articles()
        article_count = len(articles)
        logger.info("Fetched %d articles", article_count)

        signals = []
        confidence_sum = 0.0

        for article in articles:
            try:
                article["content"] = clean_text(article.get("content", ""))
                llm_result = analyze_article(article)
                clf_result = classify_article(article)

                log_metrics(
                    {
                        "classifier_score": clf_result["classifier_score"],
                        "llm_confidence": llm_result.get("confidence_score", 0.0),
                    }
                )

                logger.info(
                    "Article classified — LLM: %s | Classifier: %s (%.2f)",
                    llm_result.get("category"),
                    clf_result["classifier_category"],
                    clf_result["classifier_score"],
                )

                signal_data = {
                    "title": article.get("title", ""),
                    "source_url": article.get("url"),
                    "market": llm_result.get("market", "unknown"),
                    "category": llm_result.get("category", "other"),
                    "sentiment": llm_result.get("sentiment", "neutral"),
                    "summary": llm_result.get("summary", ""),
                    "confidence_score": float(llm_result.get("confidence_score", 0.0)),
                    "raw_text": article.get("content", "")[:2000],
                    "run_id": run_id,
                }
                signals.append(signal_data)
                confidence_sum += signal_data["confidence_score"]
            except Exception as exc:
                logger.warning("Failed to process article '%s': %s", article.get("title"), exc)

        db = get_supabase()
        if signals:
            db.table(SIGNALS_TABLE).insert(signals).execute()

        signal_count = len(signals)
        avg_confidence = round(confidence_sum / signal_count, 4) if signal_count else 0.0
        duration = round(time.time() - start_ts, 2)

        run_summary = {
            "run_id": run_id,
            "article_count": article_count,
            "signal_count": signal_count,
            "avg_confidence": avg_confidence,
            "duration_seconds": duration,
            "mlflow_run_id": mlflow_run_id,
            "status": "completed",
        }

        db.table(PIPELINE_RUNS_TABLE).insert(run_summary).execute()

        log_metrics(
            {
                "article_count": article_count,
                "signal_count": signal_count,
                "avg_confidence": avg_confidence,
                "duration_seconds": duration,
            }
        )
        end_pipeline_run(mlflow_run_id, run_summary)

        return PipelineRunResult(**run_summary)

    except Exception as exc:
        logger.error("Pipeline run failed: %s", exc)
        end_pipeline_run(mlflow_run_id, {"error": str(exc), "status": "failed"})
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {exc}")


@router.get("/status", response_model=PipelineStatus)
def get_pipeline_status():
    db = get_supabase()
    run_result = (
        db.table(PIPELINE_RUNS_TABLE).select("*").order("created_at", desc=True).limit(1).execute()
    )
    total_result = db.table(SIGNALS_TABLE).select("id", count="exact").execute()
    total_signals = total_result.count or 0

    if not run_result.data:
        return PipelineStatus(total_signals=total_signals)

    last = run_result.data[0]
    return PipelineStatus(
        last_run_id=last.get("run_id"),
        last_run_at=last.get("created_at"),
        last_run_status=last.get("status"),
        total_signals=total_signals,
    )
