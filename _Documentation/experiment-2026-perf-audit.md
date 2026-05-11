# Experiment-2026 — performance audit (post tier+cull)

The tier+cull patch holds the 30 fps render cap on average (verified at
seek=0.55, 0.80, 0.95 with the `?fps=1` overlay) but interactive
playback still feels choppy. A 500 ms moving average smears out
sub-second stalls; the audit below identifies what causes them.

## Pipeline at end-of-trip, per render frame

- `drawMinutes` — **2208 markers × 2 passes** = 4,416 `Path2D` strokes,
  each preceded by ctx.translate / .scale / inverse-translate. Pass 2
  also writes `ctx.lineWidth` per marker.
- `drawHours` — 52 strokes. Trivial.
- `drawPhotos` — up to **1,200** active. Tier+cull drops the vast
  majority to tiny on-screen sizes (<2 device px → culled, <400 px →
  thumb-tier, the rest 1024). Per drawn photo:
  - 2× `ctx.translate`, 2× `ctx.scale` (forward + inverse)
  - 3× state mutation (globalAlpha twice, strokeStyle, lineWidth) —
    **all values are identical across iterations**, the writes are
    repeated for no reason
  - 1× `ctx.strokeRect` (the #dddddd outline)
  - 1× `ctx.drawImage`
- Physics: fixed-timestep, capped at 8 ticks/frame.

## What's actually causing the choppiness

1. **First-paint JPEG decode.** `getImg` / `getThumb` set `img.src` and
   return immediately. The JPEG is fetched-then-decoded lazily. The
   **first** `drawImage(img,…)` after fetch decodes synchronously on the
   main thread — 50–200 ms per 1024-wide JPEG depending on hardware.
   During fast trip segments (parser racing, several photos activating
   per second) these decodes pile onto one frame and produce a visible
   stall. The fps average doesn't show it because the average smears
   across the 500 ms window. **Biggest single win available.**

2. **Memory eviction.** ~1,200 × 1024-wide JPEGs ≈ 180 MB on disk; once
   decoded into the raster cache each is ~2.8 MB → 3.4 GB unbounded.
   Chromium will evict under pressure and re-decode on next paint,
   producing the same stall as #1 in a "warmed up" run.

3. **Per-iteration state churn in drawPhotos.** strokeStyle, lineWidth,
   the strokeRect's static box, globalAlpha=1 between outline-and-image
   — all invariant; hoisting them out of the loop saves 1,200 × 3 = 3.6k
   state writes per frame.

4. **drawMinutes pass 1 is invariant per-marker apart from position.**
   Same strokeStyle, same alpha, same Path2D, same lineWidth.

## Fixes that preserve visual quality exactly

These don't touch any draw geometry, alpha math, or source pixels. Same
output, fewer stalls.

- **A — `img.decode()` pre-warming.** Call `img.decode()` on every
  image (full + thumb) right after setting `.src`. Decode runs async,
  the bitmap is ready before any `drawImage`. Eliminates first-paint
  stalls.
- **B — `createImageBitmap` cache. [REVERTED]** Tried decoding into
  transferable `ImageBitmap`s; bitmaps are not evicted by the browser,
  so 1,200 × 1024 photos × ~2.8 MB decoded each = ~3.4 GB resident, and
  the renderer crashes (Aw, Snap! / error 11) part way through a
  recording at the heavy end of the trip. Reverted to plain
  `HTMLImageElement`; rely on §A's `img.decode()` pre-warm to avoid the
  synchronous decode stall, and let the browser's raster cache manage
  eviction. The right form of this fix would need an LRU eviction
  policy on the bitmap cache, which is more complexity than is worth
  it given that §A alone removes most of the burst-stall.
- **C — Hoist invariant state out of drawPhotos.** Set strokeStyle,
  lineWidth-base, and the outline rect parameters once before the loop;
  inside the loop only adjust what actually varies (transform,
  globalAlpha). No visual change.
- **D — Hoist invariant state out of drawMinutes pass 1.** Same idea
  for the 2,208-marker pass.

Not applied because they would change the experience:

- Capping active photo count or fading old photos off — changes the
  "long comet tail" the experiment exists to test.
- Throttling outline draws — drops the layered see-through feel.
- Reducing source resolution — undoes the whole experiment.

## Measurement plan

- Re-run `?fps=1` capture at seek=0.55 / 0.80 / 0.95 — confirm still at
  cap.
- Side-by-side playback by eye — confirm bursts smoothed.
