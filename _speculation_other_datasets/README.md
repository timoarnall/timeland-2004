# Speculative datasets

A side-folder. Not Timeland canon.

The work in here started as one question: does the Timeland renderer still read as Timeland when given a different trip? Three datasets are built — BKK-Burma 2012, Summer 2010, Norway weekend 2013 — and answer the question yes.

## What this folder is

A spike folder. A tool spun out of the renderer to see if it generalises. The pipeline reads existing GPX archives and Sony RAW previews, writes its outputs only inside this folder, and touches nothing in `/Volumes/Groke/Photos/`.

## What this folder is not

- Not part of the 2004 Timeland port at the repo root. That artefact stayed at one trip, one essay, one embed — and is shipped.
- Not the experiment branch's mission. `experiment-2026/` is "Timeland with the 5× photo set". This folder is "Timeland with any trip".
- Not a finished tool. The renderer is a fork, the manifests are hand-tuned, the screenshots replace a real playback recording that hasn't been built yet.

## Status

- `build_dataset.py`, `render.html`, `lookup_elevation.py` — pipeline, fork of the main renderer, elevation backfill helper.
- `bkk-burma-2012/`, `summer-2010/`, `norway-weekend-2013/` — three materialised datasets with manifests, thumbs, segmented checkpoint renders.
- `CANDIDATES.md`, `FINDINGS.md` — planning report and what watching them taught me.
- `_screenshots/` — headless captures, five per dataset, plus a few debug shots from the latest changes.

## Calls available

Three reasonable next moves, picked by Timo:

- **Stop here.** Three datasets is enough to answer the question. Findings doc stands as the record.
- **Move out.** `git mv` this folder to its own repo. Different mission, different lineage.
- **Build the playback recordings.** Replace the screenshots with the same sidebyside-style video the main piece has. Lets the findings doc show, not tell.

No deadline on any of these.
