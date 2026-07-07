# Latitude-fit projection — variant note

Branch `overnight/2026-05-14-projection-latitude-aware`.

## What changed

`render.html` now accepts `?latfit=1`. When set, it computes the dataset's mean latitude and rescales longitude by `cos(centerLat) / cos(64.5°)`. The 64.5° reference is Iceland's centroid, so the main Timeland piece would render unchanged under this flag — Iceland's `G_LON_SCALE=400` was hand-tuned at that latitude.

## What it fixes

Bangkok at ~13.7°N has `cos(13.7°) ≈ 0.974`. Iceland at 64.5°N has `cos(64.5°) ≈ 0.43`. The default projection compresses every dataset by Iceland's ratio, so Bangkok comes out about 0.44× wide compared to its real proportions. Norway at ~62°N is barely affected (multiplier ≈ 1.07). Summer 2010 spans 50°N→52°N→42°N→52°N, so the mean sits around 49°N and gets a 1.51× horizontal stretch.

## Try it

```
file:///Volumes/Groke/Projects/2004 - Timeland/_speculation_other_datasets/render.html?dataset=bkk-burma-2012&latfit=1
```

Compare with and without `latfit=1` on each of the three datasets. Bangkok is the most dramatic. Norway is the most subtle.

## What to watch for

- **Bangkok.** The trip ran east-west across Thailand and north-south up the Burma border. With `latfit=0` the east-west legs look truncated; with `latfit=1` the bbox widens and the route reads as the long horizontal it actually is.
- **Summer 2010.** A 1.5× horizontal stretch over a 5-week continental span — Norway-Italy is now taller-than-wide, London leg lengthens.
- **Norway 2013.** Almost no change. Visual sanity check that the math doesn't break.

The auto-scale spring will rebalance the camera to whatever the new bounds say, so the trips don't fly off-screen. The "felt zoom level" at any given seek will read differently though — that's the point.

## Call

This is two questions, not one.

- **a. Geographic accuracy worth it?** For an archive of trips that spans 13° to 65° latitude, yes — the alternative is a renderer that says every trip happened in Iceland.
- **b. Iceland's specific look protected?** Yes by construction. The reference latitude is Iceland; running this on the main piece would show no change. The flag is opt-in per render.

If the call is "ship latfit on by default for the speculation renderer", the only change needed is flipping `LATFIT` default to `true` and removing the URL param (or inverting it to `?nofit=1`). Or leave it as it is and let the manifests declare it per-dataset.
