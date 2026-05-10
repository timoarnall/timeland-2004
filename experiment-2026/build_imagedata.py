#!/usr/bin/env python3
# Build experiment-2026/data/imageData.xml from EXIF DateTimeOriginal of the
# unfiltered originals in /Volumes/Groke/Photos/Photo Archive 2b/.
#
# Schema mirrors the archaeology data/imageData.xml: <exif> root with one
# <image><file>...</file><time>YYYY:MM:DD HH:MM:SS</time></image> per photo.
# EXIF datetimes are treated as UTC (camera was set to GPS UTC for this trip).
# Photos outside the GPX time window are dropped.

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ARCHIVE = Path("/Volumes/Groke/Photos/Photo Archive 2b")
OUT = Path(__file__).resolve().parent / "data" / "imageData.xml"

# GPX bounds for this trip (UTC).
GPX_LO = datetime(2004, 6, 30, 13, 51, 31, tzinfo=timezone.utc)
GPX_HI = datetime(2004, 7, 5,  19, 40,  8, tzinfo=timezone.utc)

# Clean stem only: 2004-MM-DD-HH-MM-SS.jpg, no hash suffix.
NAME_RE = re.compile(r"^2004-(06-30|07-0[1-6])-\d{2}-\d{2}-\d{2}\.jpg$")


def main():
    files = sorted(p for p in ARCHIVE.iterdir() if NAME_RE.match(p.name))
    print(f"clean-named candidates in trip window: {len(files)}", file=sys.stderr)

    # exiftool in one shot with -j gives a JSON array.
    cmd = ["exiftool", "-j", "-DateTimeOriginal", "-FileName", *map(str, files)]
    raw = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    data = json.loads(raw)

    candidates = []
    skipped_no_exif = 0
    skipped_out_of_window = 0
    for entry in data:
        dt_str = entry.get("DateTimeOriginal")
        if not dt_str:
            skipped_no_exif += 1
            continue
        try:
            dt = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S").replace(tzinfo=timezone.utc)
        except ValueError:
            skipped_no_exif += 1
            continue
        if dt < GPX_LO or dt > GPX_HI:
            skipped_out_of_window += 1
            continue
        candidates.append((dt, entry["FileName"]))

    # Dedupe by md5 of file content. Some photos appear twice in the archive
    # under both UTC- and CEST-derived filenames. Prefer the filename whose
    # HH-MM-SS matches its EXIF UTC time; fall back to lex-smallest.
    by_hash = {}
    for dt, name in candidates:
        with (ARCHIVE / name).open("rb") as fh:
            h = hashlib.md5(fh.read()).hexdigest()
        utc_named = name == f"{dt.strftime('%Y-%m-%d-%H-%M-%S')}.jpg"
        # Lower sort key wins. UTC-named files get priority 0, others 1.
        key = (0 if utc_named else 1, name)
        existing = by_hash.get(h)
        if existing is None or key < existing[0]:
            by_hash[h] = (key, dt, name)

    rows = sorted((dt, name) for _, dt, name in by_hash.values())

    print(f"kept after dedupe: {len(rows)} (from {len(candidates)} candidates)", file=sys.stderr)
    print(f"skipped no exif: {skipped_no_exif}", file=sys.stderr)
    print(f"skipped outside GPX window: {skipped_out_of_window}", file=sys.stderr)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("<exif>\n")
        for dt, name in rows:
            f.write(f"<image>\n<file>{name}</file>\n<time>{dt.strftime('%Y:%m:%d %H:%M:%S')}</time>\n</image>\n")
        f.write("</exif>\n")
    print(f"wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
