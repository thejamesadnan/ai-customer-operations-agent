"""Build a local, searchable knowledge index from Markdown/DOCX sources.

This script is intentionally generic. It does not contain company knowledge.
Private source files should remain local and are excluded by .gitignore.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "knowledge" / "raw"
OUTPUT = ROOT / "knowledge" / "index" / "documents.json"


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_docx(path: Path) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise SystemExit("Install the optional DOCX parser: pip install python-docx") from exc

    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def load_documents() -> list[dict]:
    documents: list[dict] = []
    if not SOURCE.exists():
        return documents

    for path in SOURCE.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() in {".md", ".markdown"}:
            text = read_markdown(path)
        elif path.suffix.lower() == ".docx":
            text = read_docx(path)
        else:
            continue

        if text.strip():
            documents.append({
                "source": str(path.relative_to(SOURCE)),
                "title": path.stem,
                "text": text,
            })

    return documents


def main() -> None:
    docs = load_documents()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Indexed {len(docs)} documents -> {OUTPUT}")


if __name__ == "__main__":
    main()
