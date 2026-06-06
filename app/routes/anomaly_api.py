from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.anomaly_service import anomaly_service, SAMPLE_TRANSACTIONS

router = APIRouter(prefix="/api/anomaly", tags=["anomaly-detection"])


class TransactionInput(BaseModel):
    amount: float
    merchant: str
    category: str
    hour: int
    day_of_week: int
    distance_from_home: float


class DetectionResult(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    confidence: float


@router.post("/detect")
async def detect_anomaly(tx: TransactionInput):
    result = anomaly_service.predict(tx.model_dump())
    return result


@router.get("/sample-transactions")
async def sample_transactions():
    return {"transactions": SAMPLE_TRANSACTIONS}


@router.get("/analyze-all")
async def analyze_all():
    predictions = anomaly_service.get_all_predictions()
    stats = anomaly_service.get_statistics()
    return {"statistics": stats, "transactions": predictions}
