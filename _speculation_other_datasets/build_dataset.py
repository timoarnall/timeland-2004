#!/usr/bin/env python3
# Build a Timeland-style dataset bundle (manifest.json + thumbs/) from
# arbitrary photo dirs + GPX files. Read-only on the archive.
#
# Run:
#   ./build_dataset.py bkk-burma-2012.json
#
# Config (one JSON file per candidate, sibling to this script):
#   {
#     "name": "bkk-burma-2012",
#     "title": "Bangkok → Burma, April 2012",
#     "photo_dirs": ["/Volumes/.../2012-04-18", ...],
#     "photo_glob": "*.arw",
#     "gpx_files": ["/Volumes/.../BKK-Burma.gpx"],
#     "date_lo": "2012-04-18T00:00:00Z",
#     "date_hi": "2012-04-28T00:00:00Z",
#     "trkpt_decimate": 1,
#     "replay_seconds": 90,
#     "accent": "#c40000"
#   }

import json
import math
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    la1, lo1 = math.radians(lat1), math.radians(lon1)
    la2, lo2 = math.radians(lat2), math.radians(lon2)
    dla = la2 - la1
    dlo = lo2 - lo1
    h = math.sin(dla/2)**2 + math.cos(la1)*math.cos(la2)*math.sin(dlo/2)**2
    return 2 * R * math.asin(math.sqrt(h))


def split_segments(pts, jump_km=100, jump_min=30):
    """Split trkpts wherever a consecutive pair has a gap > jump_km AND > jump_min
    minutes — that's a flight or other non-ground teleport. Returns list of segments,
    each a contiguous sublist of pts."""
    if not pts:
        return []
    segs = []
    cur = [pts[0]]
    for i in range(1, len(pts)):
        t0, la0, lo0, _ = pts[i-1]
        t1, la1, lo1, _ = pts[i]
        dt_min = (t1 - t0) / 1000.0 / 60.0
        d = haversine_km(la0, lo0, la1, lo1)
        if d > jump_km and dt_min > jump_min:
            segs.append(cur)
            cur = []
        cur.append(pts[i])
    if cur:
        segs.append(cur)
    return segs

HERE = Path(__file__).resolve().parent


def parse_iso(s: str) -> datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


def list_photos(photo_dirs, glob):
    out = []
    for d in photo_dirs:
        p = Path(d)
        for f in sorted(p.glob(glob)):
            out.append(f)
    return out


def extract_thumb(src: Path, dst: Path, max_w=1024, quality=70):
    """Extract embedded JPEG preview from RAW (.arw/.cr2/.nef etc) or just copy/recompress JPEG.
    Uses exiftool to pull -PreviewImage, then sips to resize+recompress.
    Returns True on success, False on skip."""
    if dst.exists():
        return True

    suffix = src.suffix.lower()
    if suffix in (".jpg", ".jpeg"):
        # Just resize/recompress
        tmp = dst.with_suffix(".raw.jpg")
        shutil.copy(src, tmp)
    else:
        # RAW: extract preview
        tmp = dst.with_suffix(".raw.jpg")
        with tmp.open("wb") as fh:
            r = subprocess.run(
                ["exiftool", "-b", "-PreviewImage", str(src)],
                stdout=fh, stderr=subprocess.DEVNULL,
            )
        if tmp.stat().st_size < 1000:
            # Try -JpgFromRaw
            tmp.unlink()
            with tmp.open("wb") as fh:
                subprocess.run(
                    ["exiftool", "-b", "-JpgFromRaw", str(src)],
                    stdout=fh, stderr=subprocess.DEVNULL,
                )
            if tmp.stat().st_size < 1000:
                tmp.unlink(missing_ok=True)
                return False

    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(quality),
         "-Z", str(max_w), str(tmp), "--out", str(dst)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    tmp.unlink(missing_ok=True)
    return dst.exists() and dst.stat().st_size > 1000


_TIME_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})"
    r"(?:\.\d+)?"
    r"(Z|[+-]\d{2}:?\d{2})?$"
)


def parse_gpx_time(s):
    m = _TIME_RE.match(s)
    if not m:
        return None
    Y, Mo, D, h, mi, se = (int(m.group(i)) for i in range(1, 7))
    off = m.group(7)
    dt = datetime(Y, Mo, D, h, mi, se, tzinfo=timezone.utc)
    if off and off != "Z":
        sign = 1 if off[0] == "+" else -1
        body = off[1:].replace(":", "")
        if len(body) >= 4:
            hh = int(body[:2]); mm = int(body[2:4])
        else:
            hh = int(body[:2]); mm = 0
        # off means local = UTC + offset → UTC = local - offset
        delta = sign * (hh * 3600 + mm * 60)
        dt = datetime.fromtimestamp(dt.timestamp() - delta, tz=timezone.utc)
    return dt


def parse_gpx_trkpts(gpx_paths):
    """Return list of (t_ms, lat, lon, ele) sorted by time."""
    pts = []
    # Tolerate either attribute order: lat then lon (Garmin) or lon then lat (Moves).
    trkpt_re = re.compile(r'<trkpt\b([^>]*)>(.*?)</trkpt>', re.DOTALL)
    attr_lat = re.compile(r'\blat="([^"]+)"')
    attr_lon = re.compile(r'\blon="([^"]+)"')
    time_re = re.compile(r"<time>([^<]+)</time>")
    ele_re = re.compile(r"<ele>([^<]+)</ele>")
    for gp in gpx_paths:
        text = Path(gp).read_text(encoding="utf-8", errors="replace")
        for m in trkpt_re.finditer(text):
            attrs = m.group(1)
            body = m.group(2)
            la = attr_lat.search(attrs)
            lo = attr_lon.search(attrs)
            if not (la and lo):
                continue
            lat, lon = la.group(1), lo.group(1)
            tm = time_re.search(body)
            if not tm:
                continue
            try:
                dt = parse_gpx_time(tm.group(1).strip())
                if dt is None:
                    continue
            except Exception:
                continue
            ele_m = ele_re.search(body)
            ele = float(ele_m.group(1)) if ele_m else 0.0
            t_ms = int(dt.timestamp() * 1000)
            pts.append((t_ms, float(lat), float(lon), ele))
    pts.sort(key=lambda p: p[0])
    # dedupe consecutive identical timestamps (same point)
    out = []
    last_t = None
    for p in pts:
        if p[0] == last_t:
            continue
        out.append(p)
        last_t = p[0]
    return out


def exif_times(files):
    """Batch read DateTimeOriginal. Returns dict {path_str: t_ms_utc_or_None}."""
    if not files:
        return {}
    cmd = ["exiftool", "-j", "-DateTimeOriginal", "-SubSecTimeOriginal",
           "-OffsetTimeOriginal", *map(str, files)]
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    data = json.loads(r.stdout or "[]")
    out = {}
    for entry in data:
        path = entry.get("SourceFile")
        dt_str = entry.get("DateTimeOriginal")
        offset = entry.get("OffsetTimeOriginal", "+00:00")
        if not (path and dt_str):
            out[path] = None
            continue
        try:
            dt = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
            # If no offset present, assume already-UTC (matches archive convention)
            if offset and offset != "+00:00":
                # Parse offset like +07:00
                sign = 1 if offset[0] == "+" else -1
                hh, mm = offset[1:].split(":")
                shift_s = sign * (int(hh) * 3600 + int(mm) * 60)
                # Convert local→UTC by subtracting offset
                dt = dt.replace(tzinfo=timezone.utc)
                dt = datetime.fromtimestamp(dt.timestamp() - shift_s, tz=timezone.utc)
            else:
                dt = dt.replace(tzinfo=timezone.utc)
            out[path] = int(dt.timestamp() * 1000)
        except Exception:
            out[path] = None
    return out


def write_per_segment_datasets(cfg, segments, parent_dir):
    """When the GPX splits into >1 segment, build one dataset per segment.
    Each becomes <name>__segN with its own manifest + thumbs."""
    base_name = cfg["name"]
    base_title = cfg.get("title", base_name)
    for i, seg in enumerate(segments):
        seg_lo = seg[0][0]
        seg_hi = seg[-1][0]
        seg_name = f"{base_name}__seg{i+1}"
        seg_iso_lo = datetime.fromtimestamp(seg_lo/1000, tz=timezone.utc).strftime("%Y-%m-%d")
        seg_iso_hi = datetime.fromtimestamp(seg_hi/1000, tz=timezone.utc).strftime("%Y-%m-%d")
        seg_cfg = dict(cfg)
        seg_cfg["name"] = seg_name
        seg_cfg["title"] = f"{base_title} — {seg_iso_lo} to {seg_iso_hi}"
        seg_cfg["date_lo"] = datetime.fromtimestamp((seg_lo - 60_000)/1000, tz=timezone.utc).isoformat()
        seg_cfg["date_hi"] = datetime.fromtimestamp((seg_hi + 60_000)/1000, tz=timezone.utc).isoformat()
        # disable further splitting on the per-segment run
        seg_cfg["split_jump_km"] = 1e9
        seg_cfg["min_segment_hours"] = 0
        tmp_path = parent_dir / f"_{seg_name}.json"
        tmp_path.write_text(json.dumps(seg_cfg, indent=2))
        print(f"  → spawning sub-build: {tmp_path.name}", file=sys.stderr)
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), str(tmp_path)])
        tmp_path.unlink(missing_ok=True)
        if r.returncode != 0:
            print(f"  WARN: seg{i+1} build returned {r.returncode}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print("usage: build_dataset.py <config.json>", file=sys.stderr)
        sys.exit(1)

    cfg_path = Path(sys.argv[1])
    cfg = json.loads(cfg_path.read_text())

    out_dir = HERE / cfg["name"]
    thumb_dir = out_dir / "thumbs"
    out_dir.mkdir(exist_ok=True)
    thumb_dir.mkdir(exist_ok=True)

    print(f"[{cfg['name']}] building", file=sys.stderr)

    # 1. GPX
    print("  reading gpx...", file=sys.stderr)
    pts = parse_gpx_trkpts(cfg["gpx_files"])
    print(f"  {len(pts)} trkpts loaded", file=sys.stderr)

    date_lo = parse_iso(cfg["date_lo"]).timestamp() * 1000
    date_hi = parse_iso(cfg["date_hi"]).timestamp() * 1000
    pts = [p for p in pts if date_lo <= p[0] <= date_hi]
    print(f"  {len(pts)} after date window", file=sys.stderr)

    # decimate
    dec = int(cfg.get("trkpt_decimate", 1))
    if dec > 1:
        pts = pts[::dec]
        print(f"  {len(pts)} after {dec}× decimate", file=sys.stderr)

    if not pts:
        print("  ERROR: no trkpts in window", file=sys.stderr)
        sys.exit(2)

    # Split into ground-only segments at any > 100 km / > 30 min gap (flight).
    jump_km = float(cfg.get("split_jump_km", 100))
    jump_min = float(cfg.get("split_jump_min", 30))
    min_seg_hours = float(cfg.get("min_segment_hours", 4))
    segments = split_segments(pts, jump_km=jump_km, jump_min=jump_min)
    segments = [s for s in segments if (s[-1][0] - s[0][0]) / 3600_000 >= min_seg_hours]
    print(f"  {len(segments)} ground-only segments after split "
          f"(jump>{jump_km}km & >{jump_min}min; min {min_seg_hours}h)",
          file=sys.stderr)
    for i, s in enumerate(segments):
        lo = datetime.fromtimestamp(s[0][0]/1000, tz=timezone.utc).isoformat()
        hi = datetime.fromtimestamp(s[-1][0]/1000, tz=timezone.utc).isoformat()
        dur_h = (s[-1][0] - s[0][0]) / 3600_000
        print(f"    seg{i+1}: {lo} → {hi}  ({len(s)} pts, {dur_h:.1f}h)", file=sys.stderr)

    if not segments:
        print("  ERROR: no segments meet minimum duration", file=sys.stderr)
        sys.exit(3)

    # If exactly one segment, fall through to single-output mode.
    # If multiple, write one dataset per segment.
    if len(segments) == 1:
        pts = segments[0]
    else:
        return write_per_segment_datasets(cfg, segments, out_dir.parent)

    gpx_lo, gpx_hi = pts[0][0], pts[-1][0]

    # 2. Photos
    print("  scanning photos...", file=sys.stderr)
    photos = list_photos(cfg["photo_dirs"], cfg["photo_glob"])
    print(f"  {len(photos)} candidate photos", file=sys.stderr)

    # Batch exiftool — chunk to avoid argv limits
    times = {}
    CHUNK = 200
    for i in range(0, len(photos), CHUNK):
        times.update(exif_times([str(f) for f in photos[i:i+CHUNK]]))

    in_window = []
    no_exif = 0
    out_of_window = 0
    for f in photos:
        t = times.get(str(f))
        if t is None:
            no_exif += 1
            continue
        if not (gpx_lo - 60_000 <= t <= gpx_hi + 60_000):
            out_of_window += 1
            continue
        in_window.append((t, f))
    in_window.sort()
    print(f"  {len(in_window)} photos in gpx window ({no_exif} no-exif, {out_of_window} out-of-window)", file=sys.stderr)

    # 3. Extract thumbs
    print(f"  extracting thumbs to {thumb_dir} ...", file=sys.stderr)
    quality = int(cfg.get("jpeg_quality", 70))
    max_w = int(cfg.get("max_w", 1024))
    out_photos = []
    failed = 0
    for i, (t, f) in enumerate(in_window):
        stem = f"{i:05d}_{f.stem.replace(' ', '_')}.jpg"
        dst = thumb_dir / stem
        ok = extract_thumb(f, dst, max_w=max_w, quality=quality)
        if not ok:
            failed += 1
            continue
        out_photos.append({"t": t, "file": stem})
        if (i + 1) % 100 == 0:
            print(f"    {i+1}/{len(in_window)}  ({failed} failed)", file=sys.stderr)
    print(f"  thumbs done: {len(out_photos)} written, {failed} failed", file=sys.stderr)

    # 4. Manifest
    manifest = {
        "name": cfg["name"],
        "title": cfg.get("title", cfg["name"]),
        "accent": cfg.get("accent", "#c40000"),
        "replay_seconds": cfg.get("replay_seconds"),
        "trkpts": [[t, lat, lon, ele] for (t, lat, lon, ele) in pts],
        "photos": out_photos,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, separators=(',', ':')))
    print(f"  wrote {out_dir/'manifest.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
