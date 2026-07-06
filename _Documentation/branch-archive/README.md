# Branch archive

Bundles of overnight/* branches, made by /branch-sweep before it clears
decided branches. Machine-local (gitignored — GitHub rejects files this
size); this volume is on Backblaze. Restore any branch with:

    git fetch _Documentation/branch-archive/overnight-<date>.bundle <branch>:<branch>
