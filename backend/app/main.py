from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import experiments, pipeline, signals

app = FastAPI(title="AfriSight API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signals.router)
app.include_router(pipeline.router)
app.include_router(experiments.router)


@app.get("/health")
def health():
    settings = get_settings()
    return {"status": "ok", "environment": settings.environment}
