from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.auth import verify_key
from app.database import get_supabase, SIGNALS_TABLE
from app.models.schemas import Signal, SignalCreate

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("", response_model=list[Signal])
def list_signals(
    market: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    sentiment: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
):
    db = get_supabase()
    query = db.table(SIGNALS_TABLE).select("*").order("created_at", desc=True).limit(limit)
    if market:
        query = query.eq("market", market)
    if category:
        query = query.eq("category", category)
    if sentiment:
        query = query.eq("sentiment", sentiment)
    result = query.execute()
    return result.data


@router.get("/{signal_id}", response_model=Signal)
def get_signal(signal_id: str):
    db = get_supabase()
    result = db.table(SIGNALS_TABLE).select("*").eq("id", signal_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Signal not found")
    return result.data[0]


@router.post("", response_model=Signal, status_code=201, dependencies=[Depends(verify_key)])
def create_signal(payload: SignalCreate):
    db = get_supabase()
    result = db.table(SIGNALS_TABLE).insert(payload.model_dump()).execute()
    return result.data[0]


@router.delete("/{signal_id}", status_code=204, dependencies=[Depends(verify_key)])
def delete_signal(signal_id: str):
    db = get_supabase()
    existing = db.table(SIGNALS_TABLE).select("id").eq("id", signal_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Signal not found")
    db.table(SIGNALS_TABLE).delete().eq("id", signal_id).execute()
