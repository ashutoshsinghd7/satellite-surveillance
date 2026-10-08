# AGENTS.md

Entry point for any AI agent (or human) about to modify this repository.
Read this file first. It tells you what else to read, and nothing more.

---

## Repository Structure

```
/
├── README.md
├── CONTEXT.md
├── PROTOTYPE.md
├── DECISIONS.md
├── AGENTS.md
├── CHECKPOINTS.md
├── docs/
│   ├── aoi.md
│   ├── datasources.md
│   └── research.md
├── src/                 # empty — no implementation yet
└── requirements.txt
```

| File | What it holds | Authoritative for |
|---|---|---|
| `README.md` | Project overview, how to set up and run | Orientation, not decisions |
| `CONTEXT.md` | Macro vision, long-term pipeline, problem statement | Why the project exists |
| `PROTOTYPE.md` | Current build scope — what's actually being built right now | What is in/out of scope for this phase |
| `DECISIONS.md` | Append-only log of real alternatives considered and rejected | Why X was chosen over Y |
| `CHECKPOINTS.md` | Task breakdown, owner, status, dependencies, output location | Current task state |
| `docs/aoi.md` | Finalized AOI bounding box + the documented landslide event it's anchored on | The AOI, once CP0 is done |
| `docs/datasources.md` | GEE collection IDs, T1/T2 date windows, DEM source, any dataset-specific notes | Which exact datasets/params are in use |
| `docs/research.md` | TerraMind integration notes, paper summaries, dead ends, anything exploratory | Reference material only — never a build spec |
| `src/` | Implementation | — empty until CP1 begins |
| `requirements.txt` | Python dependencies | — |

**No-duplication rule:** AOI coordinates live only in `docs/aoi.md`. Dataset IDs and date windows live only in `docs/datasources.md`. `PROTOTYPE.md` references these rather than repeating values. If you find a value duplicated across files, that's a bug — fix it by removing the copy, not by updating both.

---

## Minimum Reading Before Touching Anything

In order:

1. **This file.**
2. **`PROTOTYPE.md`** — current scope. Read `CONTEXT.md` instead/also only if the task is cross-cutting or touches long-term direction, not a single checkpoint.
3. **Your checkpoint's entry in `CHECKPOINTS.md`** — status, dependencies, what output is expected, what contract (schema/format) it must produce or consume.
4. **The last 3–5 entries in `DECISIONS.md`** — don't re-propose something already rejected; check the reasoning first.
5. **`docs/aoi.md` and `docs/datasources.md`** if your task touches acquisition, signals, or anything AOI/dataset-specific — use the values there, never re-derive or guess them.

Do **not** default to reading the full `DECISIONS.md` history, or `docs/research.md`, unless the task specifically requires that context (e.g. working on the TerraMind integration).

---

## Rules

- `PROTOTYPE.md` is the scope boundary. If a task seems to require something `PROTOTYPE.md` excludes, stop and flag it — don't silently expand scope.
- Every checkpoint in `CHECKPOINTS.md` is only "done" when it has a linked, inspectable output (commit/PR), not by description.
- A new real decision (alternative seriously considered and dropped) gets appended to `DECISIONS.md`. Don't skip this because it feels obvious in hindsight.
- `src/` structure, when populated, should mirror `PROTOTYPE.md`'s pipeline steps (acquisition → preprocessing → signals → fusion → storage → api → frontend), not `CONTEXT.md`'s macro intelligence layers — the prototype only implements a slice of those.
