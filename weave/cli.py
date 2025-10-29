#!/usr/bin/env python3
"""CLI entrypoint for NoteWeaver."""
import argparse
from weave.pipeline import run_pipeline
from weave.config import DEFAULT_OUTPUT_DIR, DEFAULT_MAX_WORKERS

def main():
    """Main CLI entry point."""
    ap = argparse.ArgumentParser(description="Clean OCR / ChatGPT dump into Markdown.")
    ap.add_argument("input", help="Path to input text file")
    ap.add_argument("--output", "-o", default=DEFAULT_OUTPUT_DIR, help=f"Output folder (default={DEFAULT_OUTPUT_DIR})")
    ap.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS, help=f"Concurrent LLM workers (default={DEFAULT_MAX_WORKERS})")
    args = ap.parse_args()

    run_pipeline(args.input, args.output, max_workers=args.max_workers)

if __name__ == "__main__":
    main()

