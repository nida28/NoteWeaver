"""Split raw text into per-screenshot blocks and basic cleanup."""
import re
import datetime as dt
from typing import List, Dict
from weave.config import (
    BLOCK_SPLIT_RE,
    TAKEN_RE,
    TEXT_RE,
    NOISE_PATTERNS,
)

NOISE_RE = re.compile("|".join(f"(?:{p})" for p in NOISE_PATTERNS), re.I | re.M)

def clean_noise(text: str) -> str:
    lines = []
    for ln in text.splitlines():
        if NOISE_RE.search(ln):
            continue
        lines.append(ln.strip())
    out = "\n".join(lines).strip()
    return re.sub(r'\n{3,}', '\n\n', out)

def extract_blocks(raw: str) -> List[Dict]:
    chunks = [c.strip() for c in BLOCK_SPLIT_RE.split(raw) if c.strip()]
    blocks = []
    for chunk in chunks:
        text_m = TEXT_RE.search(chunk)
        body = text_m.group(1).strip() if text_m else chunk
        date = dt.date.today()
        blocks.append({"date": date, "body": clean_noise(body)})
    return blocks
