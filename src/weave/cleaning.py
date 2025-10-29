"""LLM cleaning with concurrency and backoff."""
import os
import time
import random
import logging
from dotenv import load_dotenv
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from weave.config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    LLM_MAX_RETRIES,
    LLM_MIN_SLEEP,
    LLM_MAX_SLEEP,
    LLM_BACKOFF_BASE,
    SYSTEM_PROMPT,
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(message)s")


def clean_one(text: str, idx: int) -> str:
    attempts = 0
    while attempts < LLM_MAX_RETRIES:
        attempts += 1
        try:
            resp = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": text}],
                temperature=LLM_TEMPERATURE,
                max_tokens=LLM_MAX_TOKENS,
            )
            out = resp.choices[0].message.content.strip()
            time.sleep(random.uniform(LLM_MIN_SLEEP, LLM_MAX_SLEEP))
            return out
        except Exception as e:
            wait = LLM_BACKOFF_BASE ** attempts
            log.warning(f"[LLM] {idx}: error {e}; sleeping {wait}s")
            time.sleep(wait)
    log.error(f"[LLM] {idx}: failed after {attempts} attempts")
    return text

def clean_blocks(blocks, max_workers=None):
    from weave.config import DEFAULT_MAX_WORKERS
    if max_workers is None:
        max_workers = DEFAULT_MAX_WORKERS
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(clean_one, b["body"], i): i for i, b in enumerate(blocks)}
        for fut in as_completed(futures):
            i = futures[fut]
            try:
                results[i] = {**blocks[i], "body": fut.result()}
            except Exception as e:
                log.error(f"[LLM] Block {i} failed: {e}")
    return [results[i] for i in sorted(results.keys())]
