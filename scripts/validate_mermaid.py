#!/usr/bin/env python3
"""
Validate Mermaid diagrams in markdown files.
Checks for common syntax errors that prevent rendering.

Usage:
    python validate_mermaid.py memory/
    python validate_mermaid.py path/to/docs/target-architecture.md
"""

import re
import sys
from pathlib import Path

ERRORS = []


def extract_mermaid_blocks(filepath: Path) -> list[tuple[int, str]]:
    """Extract mermaid code blocks with their starting line numbers."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    blocks = []
    in_block = False
    block_start = 0
    block_lines = []

    for i, line in enumerate(content.split("\n"), 1):
        if line.strip() == "```mermaid":
            in_block = True
            block_start = i + 1
            block_lines = []
        elif line.strip() == "```" and in_block:
            in_block = False
            blocks.append((block_start, "\n".join(block_lines)))
        elif in_block:
            block_lines.append(line)

    return blocks


def check_diagram_type(filepath: str, line_num: int, block: str):
    """Check that the diagram type is valid standard Mermaid."""
    first_line = block.strip().split("\n")[0].strip()
    invalid_types = ["C4Context", "C4Container", "C4Component", "C4Deployment",
                     "C4Dynamic", "mindmap", "timeline", "zenuml"]
    for t in invalid_types:
        if first_line.startswith(t):
            ERRORS.append(
                f"ERROR {filepath}:{line_num} — '{t}' is not standard Mermaid. "
                f"Use 'graph TB' with styled nodes instead."
            )


def check_gantt_format(filepath: str, line_num: int, block: str):
    """Check Gantt chart date format and durations."""
    if not block.strip().startswith("gantt"):
        return

    for i, line in enumerate(block.split("\n"), line_num):
        stripped = line.strip()

        # Check dateFormat
        if stripped.startswith("dateFormat"):
            fmt = stripped.replace("dateFormat", "").strip()
            valid_formats = [
                "YYYY-MM-DD", "YYYY-MM", "DD-MM-YYYY", "DD/MM/YYYY",
                "YYYY", "X", "x"
            ]
            if fmt not in valid_formats:
                ERRORS.append(
                    f"ERROR {filepath}:{i} — Invalid dateFormat '{fmt}'. "
                    f"Use one of: {', '.join(valid_formats)}"
                )

        # Check quarter-based durations
        if re.search(r',\s*\d+q\b', stripped):
            ERRORS.append(
                f"ERROR {filepath}:{i} — Duration '{stripped.strip()}' uses 'q' "
                f"(quarters). Use 'd' (days) or 'w' (weeks) instead."
            )

        # Check YYYY-Q date values
        if re.search(r'\d{4}-Q\d', stripped):
            ERRORS.append(
                f"ERROR {filepath}:{i} — Date value uses 'YYYY-Q' format. "
                f"Use 'YYYY-MM-DD' instead."
            )


def check_unicode(filepath: str, line_num: int, block: str):
    """Check for problematic Unicode in non-label positions."""
    for i, line in enumerate(block.split("\n"), line_num):
        stripped = line.strip()

        # Skip lines where text is inside ["..."] — labels allow Unicode
        label_stripped = re.sub(r'\["[^"]*"\]', '', stripped)

        # Check subgraph labels for em/en-dash
        if stripped.startswith("subgraph") and re.search(r'[\u2013\u2014]', stripped):
            ERRORS.append(
                f"WARN {filepath}:{i} — Em/en-dash in subgraph label. "
                f"Use ASCII hyphen '-' instead."
            )

        # Check notes for Unicode arrows/symbols
        if stripped.startswith("Note") and re.search(r'[\u2192\u2190\u2191\u2193\u2714\u2716\u2705\u274C]', stripped):
            ERRORS.append(
                f"WARN {filepath}:{i} — Unicode symbol in Note. "
                f"Use ASCII text instead."
            )

        # Check participant aliases for parentheses
        if stripped.startswith("participant") and "(" in label_stripped:
            ERRORS.append(
                f"WARN {filepath}:{i} — Parentheses in participant alias. "
                f"Remove or rephrase."
            )


def check_state_transitions(filepath: str, line_num: int, block: str):
    """Check stateDiagram transitions for parentheses in labels."""
    if not block.strip().startswith("stateDiagram"):
        return

    for i, line in enumerate(block.split("\n"), line_num):
        if "-->" in line and ":" in line:
            label = line.split(":", 1)[-1].strip()
            if "(" in label or ")" in label:
                ERRORS.append(
                    f"WARN {filepath}:{i} — Parentheses in state transition label "
                    f"'{label}'. Use dashes instead."
                )


def validate_file(filepath: Path):
    """Validate all Mermaid blocks in a markdown file."""
    blocks = extract_mermaid_blocks(filepath)
    rel_path = str(filepath)

    for line_num, block in blocks:
        check_diagram_type(rel_path, line_num, block)
        check_gantt_format(rel_path, line_num, block)
        check_unicode(rel_path, line_num, block)
        check_state_transitions(rel_path, line_num, block)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_mermaid.py <path>")
        print("  <path> can be a directory or a single .md file")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        validate_file(target)
    elif target.is_dir():
        for md_file in sorted(target.rglob("*.md")):
            validate_file(md_file)
    else:
        print(f"Error: {target} not found")
        sys.exit(1)

    if ERRORS:
        print(f"\n{'='*60}")
        print(f"Found {len(ERRORS)} issue(s):\n")
        for err in ERRORS:
            print(f"  {err}")
        print(f"\n{'='*60}")
        sys.exit(1)
    else:
        blocks_count = sum(
            len(extract_mermaid_blocks(f))
            for f in (target.rglob("*.md") if target.is_dir() else [target])
        )
        print(f"\u2713 {blocks_count} Mermaid diagrams validated \u2014 no issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
