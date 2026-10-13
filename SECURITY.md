# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

The particle system editor parses untrusted `.psys`, `.emitter`, and Alembic
files. Malformed input can reach the C++ emitter extension, so treat parser
crashes as potential security issues.

Email `security@particle-system-editor.dev` with:
- editor version (`particle-editor --version`)
- a minimal crashing input
- whether the C++ emitter extension was loaded

We aim to acknowledge within 72 hours and ship a patch within 14 days for
confirmed issues.

## Out of scope

- Crashes that require a locally modified `.psys` you control
- Denial of service via intentionally huge particle counts (> 50M)
- Issues only reproducible with the debug build