from fastapi import APIRouter
from app.models.schema import Query
from app.services.cache_service import handle_query
from app.utils.metrics import metrics

router = APIRouter()

@router.post("/ask")
def ask(query: Query):
    return handle_query(query.prompt)

@router.get("/metrics")
def get_metrics():
    return metrics.summary()

@router.get("/benchmark")
def benchmark():
    return {
        "benchmark_results": metrics.summary()
    }