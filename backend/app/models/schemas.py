from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel

MarketType = Literal["ng", "ke", "tz", "cd", "et", "pan-african", "unknown"]
CategoryType = Literal["regulatory", "funding", "product_launch", "macro_risk", "payments", "other"]
SentimentType = Literal["positive", "negative", "neutral"]


class Signal(BaseModel):
    id: str
    created_at: datetime
    title: str
    source_url: Optional[str] = None
    market: MarketType = "unknown"
    category: CategoryType = "other"
    sentiment: SentimentType = "neutral"
    summary: str
    confidence_score: float = 0.0
    raw_text: Optional[str] = None
    run_id: Optional[str] = None


class SignalCreate(BaseModel):
    title: str
    source_url: Optional[str] = None
    market: MarketType = "unknown"
    category: CategoryType = "other"
    sentiment: SentimentType = "neutral"
    summary: str
    confidence_score: float = 0.0
    raw_text: Optional[str] = None
    run_id: Optional[str] = None


class PipelineRunResult(BaseModel):
    run_id: str
    article_count: int
    signal_count: int
    avg_confidence: float
    duration_seconds: float
    mlflow_run_id: str
    status: str


class PipelineStatus(BaseModel):
    last_run_id: Optional[str] = None
    last_run_at: Optional[datetime] = None
    last_run_status: Optional[str] = None
    total_signals: int = 0


class ExperimentRun(BaseModel):
    run_id: str
    run_name: Optional[str] = None
    start_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    article_count: Optional[int] = None
    signal_count: Optional[int] = None
    avg_confidence: Optional[float] = None
    prompt_version: Optional[str] = None
    model_name: Optional[str] = None
    status: str = "FINISHED"
