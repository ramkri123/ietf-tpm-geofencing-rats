#!/usr/bin/env python3
"""Convert a ---‑separated Markdown file into a one‑slide‑per‑page PDF.

Usage:  python3 md2slides.py ietf125-slides-content.md [output.pdf]

Each "---" horizontal rule in the Markdown is treated as a page break.
Speaker notes (lines starting with > **Speaker note:**) are omitted.
"""

import sys
import re
import markdown
from weasyprint import HTML

def read_slides(path):
    """Split a markdown file on top-level --- dividers, return list of slide markdown strings."""
    with open(path) as f:
        text = f.read()
    # Split on lines that are just "---" (possibly with surrounding whitespace)
    slides = re.split(r'\n---\n', text)
    # Strip speaker notes from each slide
    cleaned = []
    for s in slides:
        lines = []
        for line in s.split('\n'):
            if line.strip().startswith('> **Speaker note:'):
                continue
            lines.append(line)
        cleaned.append('\n'.join(lines).strip())
    return [s for s in cleaned if s]  # drop empties


CSS = """
@page {
    size: 254mm 190.5mm;   /* 10×7.5 in — standard 4:3 slide */
    margin: 18mm 22mm;
}
body {
    font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: 14pt;
    color: #1a1a2e;
    line-height: 1.45;
}
h1 {
    font-size: 26pt;
    color: #16213e;
    margin-top: 0;
    border-bottom: 3px solid #0f3460;
    padding-bottom: 6pt;
}
h2 {
    font-size: 22pt;
    color: #0f3460;
    margin-top: 0;
    border-bottom: 2px solid #e94560;
    padding-bottom: 4pt;
}
p strong:first-child {
    color: #0f3460;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0;
    font-size: 12pt;
}
th {
    background: #0f3460;
    color: #fff;
    padding: 6pt 10pt;
    text-align: left;
}
td {
    border: 1px solid #ccc;
    padding: 5pt 10pt;
}
tr:nth-child(even) td {
    background: #f0f4f8;
}
code, pre {
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-size: 11pt;
    background: #f0f4f8;
    border-radius: 3pt;
}
pre {
    padding: 10pt;
    border-left: 4px solid #0f3460;
    overflow-x: auto;
    white-space: pre-wrap;
}
ul, ol {
    padding-left: 18pt;
}
li {
    margin-bottom: 4pt;
}
.slide {
    page-break-after: always;
    min-height: 100%;
}
.slide:last-child {
    page-break-after: auto;
}
"""

def build_html(slides):
    """Convert list of markdown slide strings into full HTML document."""
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    parts = []
    for slide_md in slides:
        md.reset()
        html = md.convert(slide_md)
        parts.append(f'<div class="slide">{html}</div>')
    body = '\n'.join(parts)
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{body}</body>
</html>"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 md2slides.py INPUT.md [OUTPUT.pdf]", file=sys.stderr)
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src.replace('.md', '.pdf')

    slides = read_slides(src)
    print(f"Found {len(slides)} slides")

    html = build_html(slides)
    HTML(string=html).write_pdf(dst)
    print(f"Written → {dst}")


if __name__ == '__main__':
    main()
