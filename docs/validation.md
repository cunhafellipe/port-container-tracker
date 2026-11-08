# Validation evidence

Validation date: 8 November 2026. Fixtures represent June 2026 and are intentionally frozen. No historical business outcomes are inferred from this validation.

## Recorded local result

Python 3.14.10: **17 tests passed**. Chromium: **7 tests passed**. JavaScript syntax checks and Python compilation passed. The report command reproduced the committed synthetic baseline.

## Automated checks

- `make check`: Python unit/integration tests, HTTP round trips, invalid input, read/export round trip, durable state, stale-write rejection, simultaneous updates and audit-failure rollback; Python compilation; JavaScript syntax checks.
- `npm run test:e2e`: seven Chromium tests covering served brand assets, filters/empty state, responsive layouts at 390/768/1440 px the domain workflow with reload persistence, and the public showcase.
- `make report`: baseline JSON and CSV generated from the same domain calculations used by the browser.

Domain coverage: Known ISO check digit, invalid identifiers, held release, clearance reason, full state machine, exact dwell boundary and departed dwell.

## Browser review

The native browser entry point reported no browser available, so review used the shared Playwright browser. The core flow was exercised through real forms and buttons against the local Python server. Reload persistence, visible success and rejection messages, record selection and mobile document width were checked. Screenshots are actual rendered pages, not design mockups.

1. Select MSCU1000017 and try to release it. The active customs hold blocks the transition.
2. Enter a fictional customs clearance reference, clear the hold, release the container, then record gate out.
3. Reload and select the same identifier. Its completed journey and frozen dwell remain available; inspect the activity log.

See [desktop screenshot](preview.png), [mobile screenshot](mobile.png), and the current [GitHub Actions run](https://github.com/phlppgdfry/port-container-tracker/actions/workflows/demo.yml). The badge reports the remote result; this document describes the checks, not an invented production certification.

## Limits of the evidence

The suite tests a local single-workspace product with synthetic records. It does not establish external integration reliability, real user outcomes, scale, production security, legal compliance or clinical validity. No terminal operating system, EDI endpoint, AIS/vessel feed, real customs clearance or Oracle warehouse is connected. Clearing a hold is a simulation action in one trusted local workspace.
