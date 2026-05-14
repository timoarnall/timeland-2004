#!/usr/bin/env python3
# Look up missing elevation in a manifest.json using Norwegian Kartverket's
# free hoydedata point service. Caches results by rounded (lat, lon).
# Only writes elevation back where it's currently 0.
#
# Run: ./lookup_elevation.py norway-weekend-2013

import json
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

API = "https://ws.geonorge.no/hoydedata/v1/punkt"

HERE = Path(__file__).resolve().parent


def fetch(lat, lon, retries=3):
    url = f"{API}?koordsys=4326&ost={lon:.6f}&nord={lat:.6f}"
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                data = json.loads(r.read())
            if data.get("punkter"):
                z = data["punkter"][0].get("z")
                if z is None:
                    return None
                return float(z)
            return None
        except Exception:
            if attempt == retries - 1:
                return None
            time.sleep(0.5 * (attempt + 1))


def main():
    if len(sys.argv) < 2:
        print("usage: lookup_elevation.py <dataset_name>", file=sys.stderr)
        sys.exit(1)

    ds = sys.argv[1]
    mfp = HERE / ds / "manifest.json"
    m = json.loads(mfp.read_text())
    ts = m["trkpts"]
    print(f"[{ds}] {len(ts)} trkpts, current with elevation: "
          f"{sum(1 for p in ts if p[3] != 0)}", file=sys.stderr)

    # Dedupe by rounded (lat, lon) to 5 decimals (~1 m horizontally).
    keys = {}
    for p in ts:
        k = (round(p[1], 5), round(p[2], 5))
        keys.setdefault(k, None)
    print(f"  unique points: {len(keys)}", file=sys.stderr)

    done = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch, lat, lon): (lat, lon)
                   for (lat, lon) in keys}
        for fut in as_completed(futures):
            (lat, lon) = futures[fut]
            try:
                z = fut.result()
            except Exception:
                z = None
            keys[(lat, lon)] = z
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(keys)}", file=sys.stderr)

    missing = sum(1 for v in keys.values() if v is None)
    print(f"  fetched: {len(keys) - missing} ok, {missing} failed",
          file=sys.stderr)

    for p in ts:
        k = (round(p[1], 5), round(p[2], 5))
        z = keys.get(k)
        if z is not None:
            p[3] = z

    mfp.write_text(json.dumps(m, separators=(",", ":")))
    (HERE / ds / "manifest.js").write_text(
        f"window.__MANIFEST = {json.dumps(m, separators=(',', ':'))};"
    )
    print(f"  wrote {mfp}", file=sys.stderr)


if __name__ == "__main__":
    main()
