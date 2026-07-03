import time
import logging
import requests

from app.utils.metrics import metrics

logger = logging.getLogger(__name__)

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

    logger.info("Calling LLM...")

    response_text = call_llm(prompt)

    latency = time.time() - start_time

    metrics.record_miss(latency)

    return {
        "source": "llm",
        "response": response_text,
        "latency_seconds": round(latency, 4)
    }