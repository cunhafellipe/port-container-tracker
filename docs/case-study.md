# Quay / Container Tracker — delivery case study

## Problem and intended user

Terminal teams need to distinguish a long-dwelling container from a container that is actually eligible for release.

## Delivered vertical slice

A terminal operations simulation with ISO 6346 checks, customs-gated release, dwell exceptions and an auditable arrival-to-gate journey.

1. Select MSCU1000017 and try to release it. The active customs hold blocks the transition.
2. Enter a fictional customs clearance reference, clear the hold, release the container, then record gate out.
3. Reload and select the same identifier. Its completed journey and frozen dwell remain available; inspect the activity log.

## Acceptance criteria mapped to evidence

| Criterion | Verification |
| --- | --- |
| A reviewer can run the product without external credentials | `python3 -m demo.server`; standard-library runtime |
| Domain constraints are enforced on the server | `tests/test_demo_domain.py`; invalid transitions and boundary cases |
| Successful actions survive a new connection | `PersistenceTests.test_mutation_persists_and_is_audited` |
| A stale edit cannot overwrite newer state | Version conflict and simultaneous update tests |
| An audit write failure leaves the record unchanged | Fault-injected SQLite audit failure test |
| The main task works through the rendered interface | Domain workflow in `tests/browser/workspace.spec.cjs` |
| The interface works at mobile and desktop widths | 390, 768 and 1440 px browser tests; screenshots in `docs/` |
| Reported numbers can be reproduced | `python3 -m demo.report`; committed baseline JSON and CSV |

Domain-specific evidence: Known ISO check digit, invalid identifiers, held release, clearance reason, full state machine, exact dwell boundary and departed dwell.

## What this demonstrates

Requirements are reduced to a coherent executable workflow, rather than a catalogue of disconnected features. Input contracts, state ownership, failure states, persistence and explanations are part of the product. Design choices and operational limits are recorded so another engineer can inspect the implementation and reproduce its behaviour.

## What it does not prove

No terminal operating system, EDI endpoint, AIS/vessel feed, real customs clearance or Oracle warehouse is connected. Clearing a hold is a simulation action in one trusted local workspace.

No user study, commercial result, uptime, production scale, legal compliance or measured improvement is claimed. The historical concept is context, not evidence.
