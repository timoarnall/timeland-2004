# Scope question — preservation, or engine?

Five briefings (2026-05-11 → 2026-05-15) have named the same drift without
making it a decision. Writing it down so it's decidable.

## What happened

The 2026 work began as preservation. Port the 2004 Flash piece to HTML so
it still runs. That core is shipped at `index.html`, archived in
`_Documentation/2026-archaeology.md`, and quiet.

The `experiment-2026/` thread asked one local question: does feeding 1200
unedited photos instead of the curated 241 change the reading. That stayed
inside the preservation arc.

`_speculation_other_datasets/` is something else. Three trips, eleven
playable segments, a forked renderer, a generic builder, an elevation
helper, a findings doc. The engine works on Bangkok, on a Norway-Italy-
London arc, on an Oppdal weekend. It is a "Timeland engine" now, not a
"Timeland of Iceland 2004" port.

## Three readings

**A. Preservation only.** Archive the engine work as a one-off speculative
spike and move on. The 2004 piece stays the project. `_speculation_other_datasets/`
gets a freeze note in its README and stops growing. The project's identity
stays clear: a faithful HTML port of a 2004 work.

Cost: throws away a working multi-dataset rig that took real time to build.

**B. Both, side by side.** Keep `index.html` as the preservation. Keep
`_speculation_other_datasets/` as the engine playground. Add a project-root
note that names both surfaces and explains why they coexist. No structural
change beyond clearer signage.

Cost: the folder name `_speculation_other_datasets/` lies about what it is
now. It is no longer speculation, it's a working tool. Rename or accept the
mismatch.

**C. Generalised atlas.** Promote the engine. The repo becomes a renderer
for time-and-place datasets, and 2004 Iceland is one input among several.
`index.html` becomes a landing page that lists every dataset, including
the 2004 one. The current root `index.html` moves to `iceland-2004/`.

Cost: the preservation surface gets folded into a multi-piece site. The
2004 work loses its standalone-piece reading and becomes one tile in an
atlas. Hard to undo cleanly once the URLs change.

## Where the folder lives, under each reading

Independent of A/B/C, the folder location resolves:

- **Subfolder of this repo** (current). Cheapest. Couples preservation and
  engine in one git history, which is wrong under reading A and ambiguous
  under reading B.
- **Separate repo `timeland-engine/`**. Cleanest under reading B. Repo
  identity matches surface identity. Costs a `git filter-branch` to keep
  history, or accepts a clean cut.
- **Promoted to root** (reading C). The engine becomes the project; 2004
  becomes a dataset.

## The decision shape

A is a deletion. B is a renaming and a note. C is a restructure.

The longer it stays uncalled, the more reading C costs to undo, because
every new dataset hardens the engine into the repo.

## What's not in this question

- Whether the engine is interesting (yes, per `FINDINGS.md`).
- Whether the preservation is finished (yes, per `_Documentation/2026-archaeology.md`).
- Whether latitude-aware projection ships (separate question, separate
  branch).
- Whether place names, heart-rate, or other event types get rendered
  (downstream of whichever reading wins).
