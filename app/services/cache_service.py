import json
import time
import logging
import requests

from app.core.redis_client import redis_client
from app.services.embedding import get_embedding
from app.utils.similarity import cosine_similarity
from app.utils.metrics import metrics

logger = logging.getLogger(__name__)

SIMILARITY_THRESHOLD = 0.90
OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


def handle_query(prompt: str):

    logger.info(f"Incoming request: {prompt}")

    start_time = time.time()
    query_embedding = get_embedding(prompt)

    # ✅ Cache lookup
    for key in redis_client.keys():
        cached = json.loads(redis_client.get(key))
        similarity = cosine_similarity(query_embedding, cached["embedding"])

        if similarity > SIMILARITY_THRESHOLD:
            latency = time.time() - start_time

            logger.info("✅ Cache HIT")
            logger.info(f"Latency: {latency:.4f}s")

            metrics.record_hit(latency)

            return {
                "source": "cache",
                "response": cached["response"],
                "latency_seconds": round(latency, 4)
            }

    # ✅ Cache miss
    logger.info("❌ Cache MISS - Calling LLM")

    llm_start = time.time()
    response_text = call_llm(prompt)
    llm_latency = time.time() - llm_start

    redis_client.set(
        prompt,
        json.dumps({
            "embedding": query_embedding,
            "response": response_text
        })
    )

    total_latency = time.time() - start_time

    logger.info(f"LLM Time: {llm_latency:.4f}s")
    logger.info(f"Total Time: {total_latency:.4f}s")

    metrics.record_miss(total_latency)

    return {
        "source": "llm",
        "response": response_text,
        "latency_seconds": round(total_latency, 4),
        "llm_inference_seconds": round(llm_latency, 4)
    }