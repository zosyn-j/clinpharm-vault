from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUT_JSON = BASE_DIR / "inventories" / "dispute_index.json"
OUT_MD = BASE_DIR / "inventories" / "dispute_index.md"

PATTERNS = {
    "DISPUTE": re.compile(r"\[DISPUTE(?::[^\]]*)?\]", re.IGNORECASE),
    "NEEDS REVIEW": re.compile(r"\[NEEDS REVIEW(?::[^\]]*)?\]", re.IGNORECASE),
    "SOURCE NEEDED": re.compile(r"\[SOURCE NEEDED(?::[^\]]*)?\]", re.IGNORECASE),
    "HTML COMMENT": re.compile(r"<!--\s*(DISPUTE|NEEDS REVIEW|SOURCE NEEDED):.*?-->", re.IGNORECASE),
}

SKIP_PARTS = {"raw", ".git", "__pycache__", "inventories", "docs", "templates"}


def should_scan(path: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False
    if path.name == "README.md" and path.parent == BASE_DIR:
        return False
    if path.name == "index.md" and 'disputes' in path.parts:
        return False
    return not any(part in SKIP_PARTS for part in path.parts)


def main():
    findings = []
    for path in sorted(BASE_DIR.rglob("*.md")):
        if not should_scan(path):
            continue
        rel_path = path.relative_to(BASE_DIR)
        lines = path.read_text(errors="ignore").splitlines()
        for idx, line in enumerate(lines, start=1):
            hits = [label for label, pattern in PATTERNS.items() if pattern.search(line)]
            if hits:
                findings.append(
                    {
                        "path": str(rel_path),
                        "line": idx,
                        "tags": hits,
                        "text": line.strip(),
                    }
                )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_dir": str(BASE_DIR),
        "count": len(findings),
        "findings": findings,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")

    lines = [
        "# Dispute and review index",
        "",
        f"- Generated: {payload['generated_at']}",
        f"- Findings: {payload['count']}",
        "- Scope: knowledge-content Markdown files under the ClinPharm vault, excluding `raw/`, `inventories/`, `docs/`, and `templates/`.",
        "",
    ]
    if findings:
        lines.extend([
            "| File | Line | Tag(s) | Text |",
            "|---|---:|---|---|",
        ])
        for item in findings:
            tags = ", ".join(item["tags"])
            text = item["text"].replace("|", "\\|")
            lines.append(f"| `{item['path']}` | {item['line']} | {tags} | {text} |")
    else:
        lines.append("No dispute or review tags found.")

    OUT_MD.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
