"""Remove duplicate or near-duplicate blocks."""
import difflib
import hashlib
from weave.config import DEDUP_SIMILARITY_THRESHOLD

def canonical(p: str) -> str:
    return " ".join(p.lower().split())

def hash_text(p: str) -> str:
    return hashlib.md5(canonical(p).encode()).hexdigest()

def dedup_blocks(blocks):
    seen = []
    unique = []
    for b in blocks:
        body = b["body"]
        h = hash_text(body)
        if any(difflib.SequenceMatcher(None, canonical(body), s).ratio() > DEDUP_SIMILARITY_THRESHOLD for s in seen):
            continue
        seen.append(canonical(body))
        unique.append(b)
    return unique
