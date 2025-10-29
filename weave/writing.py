"""Write cleaned blocks into Markdown files (one per day)."""
from pathlib import Path
import datetime as dt
from weave.config import DATE_FORMAT, DATE_HEADER_FORMAT

def write_blocks(blocks, output_dir: Path):
    files_written = []
    by_date = {}
    for b in blocks:
        by_date.setdefault(b["date"], []).append(b)

    for date, entries in by_date.items():
        fname = date.strftime(DATE_FORMAT) + ".md"
        path = Path(output_dir) / fname
        entries = list(entries)
        entries.sort(key=lambda e: e.get("time") or dt.time(0, 0))

        lines = [f"# {date.strftime(DATE_HEADER_FORMAT)}", ""]
        for e in entries:
            lines += ["#### Time", "", e["body"], "", "---", ""]
        path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        files_written.append(path)
    return files_written
