"""Glue: parse → clean → dedup → write."""
from pathlib import Path
from weave.parsing import extract_blocks
from weave.cleaning import clean_blocks
from weave.dedup import dedup_blocks
from weave.writing import write_blocks

def run_pipeline(input_path: str, output_dir: str, max_workers: int = None):
    from weave.config import DEFAULT_MAX_WORKERS
    if max_workers is None:
        max_workers = DEFAULT_MAX_WORKERS
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw = input_path.read_text(encoding="utf-8", errors="ignore")
    print(f"🔹 Loaded {input_path}")

    blocks = extract_blocks(raw)
    print(f"🔹 Parsed {len(blocks)} blocks")

    cleaned = clean_blocks(blocks, max_workers=max_workers)
    print(f"🔹 Cleaned {len(cleaned)} blocks")

    deduped = dedup_blocks(cleaned)
    print(f"🔹 Deduplicated → {len(deduped)} unique blocks")

    written = write_blocks(deduped, output_dir)
    print(f"✅ Wrote {len(written)} file(s) to {output_dir}")
