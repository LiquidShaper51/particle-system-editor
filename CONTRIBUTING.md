# Contributing to particle-system-editor

Thanks for wanting to help build the particle system editor. This project is a
Windows desktop tool written in Python (with an optional C++ emitter extension)
for authoring, previewing, and exporting particle systems.

## Ground rules

- One feature per pull request. Keep diffs scoped.
- Every new handler/processor/driver pair needs at least one fixture under
  `tests/fixtures/`.
- Run `pytest` and `ruff` before opening a PR. CI runs both.
- Type hints are required on all public functions.

## Development setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pre-commit install
```

## Architecture overview

The editor is a **pipeline**: ingest handlers read a source format and emit a
normalized `ParticleGraph`, processors mutate/optimize that graph, and output
drivers serialize it to a target format. Jobs are scheduled by the `JobRunner`
in `services/`.

```
handlers/  ->  processors/  ->  drivers/
        \        |          /
         models/ (shared schema)
```

## Commit style

`area: short imperative summary` — e.g. `handlers: support Alembic v2 emit`.

## Reporting issues

Include the editor version, the source file format, and a minimal repro. Attach
the offending `.psys` if possible.