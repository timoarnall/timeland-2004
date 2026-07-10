#!/usr/bin/env python3
"""Render the lay essay as a reading page with the same chrome as the technical one.

The lay draft lives in the elasticspace project as an HTML fragment: no head,
no body, h2-delimited, with three comparison GIFs referenced by the paths they
will have once published. This copies the fragment, rewrites those paths to a
vendored media folder next to the output, and wraps the result in the reader
chrome from build_essay_reader (read marks, notes, copy-back footer).

Read state is keyed separately from the technical essay, so marking one read
does not mark the other.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_essay_reader import CSS, JS, controls, slug  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(
    "/Volumes/Groke/Projects/2026 - Elasticspace update/01-content/drafts/"
    "draft-timeland-archaeology-2026.html"
)
MEDIA_SRC = Path(
    "/Volumes/Groke/Projects/2026 - Elasticspace update/01-content/source-images/"
    "timeland-archaeology"
)
OUT = ROOT / "_Documentation" / "2026-archaeology-lay.html"
MEDIA_OUT = ROOT / "_Documentation" / "lay-essay-media"

KEY = "timeland-lay-essay-read-v1"
TITLE = "Time that land forgot, an archaeology"
INTRO_TITLE = "Opening"


def vendor_media(fragment):
    """Copy referenced GIFs next to the output; rewrite src to a relative path."""
    MEDIA_OUT.mkdir(parents=True, exist_ok=True)
    names = set(re.findall(r'src="[^"]*/([^"/]+\.gif)"', fragment))
    missing = [n for n in names if not (MEDIA_SRC / n).exists()]
    if missing:
        sys.exit(f"missing media: {', '.join(sorted(missing))}")
    for n in sorted(names):
        shutil.copy2(MEDIA_SRC / n, MEDIA_OUT / n)
    fragment = re.sub(
        r'src="[^"]*/([^"/]+\.gif)"', r'src="lay-essay-media/\1"', fragment
    )
    return fragment, sorted(names)


def split_sections(fragment):
    """Split an h2-delimited fragment into [(title, inner_html)], intro first."""
    parts = re.split(r"<h2>(.*?)</h2>", fragment, flags=re.S)
    intro = parts[0].strip()
    out = []
    if intro:
        out.append((INTRO_TITLE, intro))
    for i in range(1, len(parts), 2):
        out.append((re.sub(r"<[^>]+>", "", parts[i]).strip(), parts[i + 1].strip()))
    return out


def main():
    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    fragment = SRC.read_text(encoding="utf-8")
    fragment = re.sub(r"<!--.*?-->", "", fragment, flags=re.S).strip()
    fragment, media = vendor_media(fragment)

    sections = split_sections(fragment)
    toc, body = [], []
    for title, inner in sections:
        sid = slug(title)
        toc.append({"id": sid, "title": title})
        heading = "" if title == INTRO_TITLE else f"<h2>{html.escape(title)}</h2>"
        body.append(
            f'<section id="{sid}">'
            f'<div class="shead">{heading}{controls(sid)}</div>'
            f"{inner}</section>"
        )

    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", fragment, flags=re.S | re.I)
    words = len(html.unescape(re.sub(r"<[^>]+>", " ", text)).split())

    nav = "\n".join(f'<a href="#{s["id"]}">{html.escape(s["title"])}</a>' for s in toc)
    js = (
        JS.replace("__TOC__", json.dumps(toc))
        .replace("timeland-archaeology-read-v1", KEY)
        .replace(
            "Timeland archaeology essay — my pass, ",
            "Timeland lay essay (the version for readers) — my pass, ",
        )
    )
    page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TITLE)} — the lay essay</title>
<style>{CSS}
figure{{margin:1.8rem 0}}
figure img{{width:100%;height:auto;border-radius:4px;display:block}}
figcaption{{color:var(--dim);font-size:.82em;margin:.5rem 0 0;line-height:1.5}}
hr{{border:none;border-top:1px solid var(--faint);margin:3rem 0}}
</style>
</head><body>
<div id="bar"></div>
<div class="wrap">
<nav><h3>Contents</h3>{nav}</nav>
<main><h1>{html.escape(TITLE)}</h1>{"".join(body)}</main>
</div>
<div id="foot">
  <span class="count"><b>0</b> of {len(toc)} sections read</span>
  <span class="count">{words:,} words &middot; the lay version</span>
  <span class="spacer"></span>
  <button id="reset" type="button">Reset</button>
  <button id="copy" type="button">Copy for Claude</button>
</div>
<script>{js}</script>
</body></html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(
        f"wrote {OUT.relative_to(ROOT)}  "
        f"({len(toc)} sections, {words:,} words, {len(page):,} bytes, "
        f"{len(media)} gifs vendored)"
    )


if __name__ == "__main__":
    main()
