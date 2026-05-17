# Scope sketches — A, B, C made concrete

Companion to `_Documentation/experiment-scope-question.md`
(on `overnight/2026-05-16-scope-question`). That doc names the three
readings in prose. This one writes out, for each, what the first 30
minutes of follow-through looks like: the file tree after the move, the
README opening paragraph, the exact set of `git mv` / `mkdir` calls, and
one line on what's lost and gained.

The point is to make the readings comparable side by side instead of
holding three folder layouts in your head.

---

## Reading A — preservation only

The 2004 piece stays the project. The engine work is frozen as a spike.

### Tree after

```
README.md
index.html
data/
experiment-2026/
_archive_2004/
_Documentation/
_speculation_other_datasets/
  README.md           <- new: freeze note, last-iteration date, why
  (everything else untouched and read-only by convention)
```

### README opening paragraph (project root, unchanged)

> *Time that land forgot* — a 2026 HTML port of a 2004 Flash piece about
> a road trip around Iceland. The original .swf is in `_archive_2004/`;
> the port is `index.html`; the archaeology of the port is in
> `_Documentation/2026-archaeology.md`.

### `_speculation_other_datasets/README.md` opening (new)

> A spike that asked whether the renderer generalises to other trips.
> Yes — see `FINDINGS.md`. Three datasets are wired up
> (`bkk-burma-2012`, `summer-2010`, `norway-weekend-2013`). The spike is
> frozen as of 2026-05-17; the project's surface is `index.html`.

### File moves

```
# none — pure addition of one README
touch _speculation_other_datasets/README.md
```

### What's lost / what's gained

Lost: an active multi-dataset rig. Gained: a clear identity for the
project (one piece, one port, one URL).

---

## Reading B — both, side by side

Preservation and engine coexist. The folder gets a name that doesn't
lie.

### Tree after

```
README.md                        <- adds a "Two surfaces" section
index.html
data/
experiment-2026/
_archive_2004/
_Documentation/
timeland-engine/                 <- renamed from _speculation_other_datasets/
  README.md                      <- new: what this is, how to add a dataset
  render.html
  build_dataset.py
  lookup_elevation.py
  FINDINGS.md
  CANDIDATES.md
  bkk-burma-2012/  ...
  summer-2010/  ...
  norway-weekend-2013/  ...
```

### README opening paragraph (project root, revised)

> *Time that land forgot* is two surfaces in one repo. **The piece**
> (`index.html`) is the 2026 HTML port of the 2004 Flash work about a
> road trip around Iceland. **The engine** (`timeland-engine/`) is the
> same renderer turned generic — it takes a GPX-and-photos dataset and
> plays it back. Three datasets are wired up so far. The piece is the
> work; the engine is what the work became when it generalised.

### `timeland-engine/README.md` opening (new)

> A renderer for time-and-place datasets. Forked from the 2004 Iceland
> piece (`../index.html`) when it became clear the same machinery worked
> on other trips. Add a dataset by writing a `*.json` manifest pointing
> at GPX + photo paths, then opening
> `render.html?dataset=<name>`. See `FINDINGS.md` for what each dataset
> revealed.

### File moves

```
git mv _speculation_other_datasets timeland-engine
# then add the new README and edit the root README to add the "Two surfaces" section
```

### What's lost / what's gained

Lost: nothing structural; URLs from `_speculation_other_datasets/` rot
(internal only). Gained: the folder name matches what it does. No
restructure of the preservation surface.

---

## Reading C — generalised atlas

The engine is promoted to the project. 2004 Iceland is one dataset
among several. `index.html` becomes an atlas landing page.

### Tree after

```
README.md                <- rewritten: atlas, not piece
index.html               <- new: dataset list (was iceland-2004's renderer)
render.html              <- promoted from _speculation_other_datasets/
build_dataset.py
lookup_elevation.py
FINDINGS.md
CANDIDATES.md
datasets/
  iceland-2004/          <- the 2004 work, now one of N
    index.html           <- the old root index.html, moved here
    data/                <- moved from project root
    experiment-2026/     <- moved here too (still a 2004 dataset variant)
    _archive_2004/       <- the original Flash work, archive
  bkk-burma-2012/        <- moved from _speculation_other_datasets/
  summer-2010/
  norway-weekend-2013/
_Documentation/          <- stays at root
```

### README opening paragraph (project root, rewritten)

> An atlas of trips rendered from GPX and photographs. The renderer
> grew out of a 2026 HTML port of a 2004 Flash piece about a road trip
> around Iceland (`datasets/iceland-2004/`). It now plays back any
> dataset with the same shape — a GPX track, timestamped photos, a
> manifest. See `index.html` for the dataset list.

### File moves

```
mkdir datasets
git mv index.html datasets/iceland-2004/index.html
git mv data datasets/iceland-2004/data
git mv experiment-2026 datasets/iceland-2004/experiment-2026
git mv _archive_2004 datasets/iceland-2004/_archive_2004
git mv _speculation_other_datasets/render.html ./render.html
git mv _speculation_other_datasets/build_dataset.py ./build_dataset.py
git mv _speculation_other_datasets/lookup_elevation.py ./lookup_elevation.py
git mv _speculation_other_datasets/FINDINGS.md ./FINDINGS.md
git mv _speculation_other_datasets/CANDIDATES.md ./CANDIDATES.md
git mv _speculation_other_datasets/bkk-burma-2012 datasets/bkk-burma-2012
git mv _speculation_other_datasets/summer-2010 datasets/summer-2010
git mv _speculation_other_datasets/norway-weekend-2013 datasets/norway-weekend-2013
rmdir _speculation_other_datasets
# then write the new root index.html (atlas listing) and rewrite README.md
```

### What's lost / what's gained

Lost: the 2004 piece's standalone-work reading. Its URL changes —
`timoarnall.github.io/timeland-2004/` no longer opens the piece, it
opens an atlas. The piece becomes
`timoarnall.github.io/timeland-2004/datasets/iceland-2004/`. Lost: the
archaeology doc's "this is the project" framing — would need rewording.

Gained: a clean identity for what the repo actually is now. New
datasets cost almost nothing to add. The engine stops hiding under a
`_speculation_` prefix.

---

## Side-by-side: the cost of waiting

A is reversible at any time (it's a deletion; the engine can be revived
from git). B is reversible (a folder rename and a README edit).

C gets more expensive each week. Every new dataset hardens the engine
into the repo and every external link to a dataset under
`_speculation_other_datasets/` will need redirecting if the structure
changes later.

The order of difficulty to reverse, today, is C > B > A. If you're
leaning toward C, doing it sooner is cheaper than doing it later.
