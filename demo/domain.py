from demo.contracts import text, record, metric


from datetime import datetime, timezone
import re

AS_OF = datetime(2026, 6, 16, 8, tzinfo=timezone.utc)
STEPS = ["arrived", "yard", "released", "gate_out"]


def valid_container_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Z]{3}[UJZ][0-9]{7}", value):
        return False
    letters = dict(
        zip(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            [
                10,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
                32,
                34,
                35,
                36,
                37,
                38,
            ],
        )
    )
    checksum = (
        sum(
            (int(c) if c.isdigit() else letters[c]) * 2**i
            for i, c in enumerate(value[:10])
        )
        % 11
        % 10
    )
    return checksum == int(value[-1])


CONFIG = {
    "columns": [
        ["name", "Container"],
        ["status", "Milestone"],
        ["value", "Dwell"],
        ["context", "Yard block"],
    ],
    "title": "Quay / Container Tracker",
    "heading": "Every container. A clear next move.",
    "subtitle": "Follow the yard-to-gate journey, surface dwell exceptions, and release cargo only when customs allows it.",
    "section": "Terminal operations",
    "list_title": "Container register",
    "theme": "port",
    "port": 8112,
    "clock": "Simulation clock · 16 June 2026, 08:00 UTC",
}


ACTIONS = frozenset(["advance", "clear_hold"])


def seed():
    result = []
    for i, (state, hold, arrived, block, vessel, teu) in enumerate(
        [
            (
                "yard",
                False,
                "2026-06-10T08:00:00+00:00",
                "B-04",
                "North Sea Express",
                2,
            ),
            ("yard", True, "2026-06-08T08:00:00+00:00", "A-12", "Baltic Horizon", 2),
            (
                "arrived",
                False,
                "2026-06-16T06:00:00+00:00",
                "Quay",
                "North Sea Express",
                1,
            ),
            (
                "released",
                False,
                "2026-06-12T08:00:00+00:00",
                "C-02",
                "Atlantic Bridge",
                2,
            ),
            (
                "gate_out",
                False,
                "2026-06-13T08:00:00+00:00",
                "Outside",
                "Baltic Horizon",
                1,
            ),
            ("yard", False, "2026-06-15T08:00:00+00:00", "B-08", "Atlantic Bridge", 2),
            ("arrived", True, "2026-06-16T04:00:00+00:00", "Quay", "Baltic Horizon", 2),
            (
                "yard",
                False,
                "2026-06-09T08:00:00+00:00",
                "C-06",
                "North Sea Express",
                1,
            ),
        ]
    ):
        prefix = f"MSCU{100000 + i}"
        identifier = next(
            prefix + str(n) for n in range(10) if valid_container_id(prefix + str(n))
        )
        result.append(
            dict(
                id=identifier,
                name=identifier,
                state=state,
                hold=hold,
                arrived=arrived,
                block=block,
                vessel=vessel,
                teu=teu,
                departed="2026-06-15T08:00:00+00:00" if state == "gate_out" else None,
            )
        )
    return result


def dwell(r):
    until = datetime.fromisoformat(r["departed"]) if r["departed"] else AS_OF
    return (until - datetime.fromisoformat(r["arrived"])).total_seconds() / 86400


def present(records):
    return [
        r
        | {
            "status": r["state"].replace("_", " ").title(),
            "value": f"{dwell(r):.1f} days",
            "context": r["block"],
            "exception": r["state"] != "gate_out" and dwell(r) > 5,
        }
        for r in sorted(records, key=dwell, reverse=True)
    ]


def metrics(records):
    yard = [r for r in records if r["state"] != "gate_out"]
    return [
        metric("On terminal", len(yard), "Excludes gate-out containers"),
        metric("TEU on terminal", sum(r["teu"] for r in yard), "20 ft = 1; 40 ft = 2"),
        metric(
            "Dwell exceptions",
            sum(dwell(r) > 5 for r in yard),
            "Strictly more than 5 days",
        ),
        metric(
            "Customs holds",
            sum(r["hold"] for r in yard),
            "Release is blocked while held",
        ),
    ]


def analysis(records):
    active = [r for r in records if r["state"] != "gate_out"]
    bars = []
    for vessel in sorted({r["vessel"] for r in active}):
        members = [r for r in active if r["vessel"] == vessel]
        mean_days = sum(dwell(r) for r in members) / len(members)
        # Python versions can differ in float summation precision. Publish a
        # deliberate precision contract instead of raw intermediate floats.
        bars.append(
            {
                "label": vessel,
                "value": round(min(100, mean_days * 10), 4),
                "display": f"{mean_days:.1f} d",
            }
        )
    return {
        "title": "Release with confidence.",
        "headline": f"{sum(r['hold'] for r in active)} containers need customs clearance.",
        "description": "Follow a validated state machine from arrival to gate out. Customs holds block release; every committed action leaves an audit entry. No live vessel feed is connected.",
        "bars_title": "Mean dwell by vessel · days (10-day scale)",
        "bars": bars,
    }


def execute(records, p):
    r = record(records, p)
    if not valid_container_id(r["id"]):
        raise ValueError("Invalid ISO 6346 identifier")
    if p["action"] == "advance":
        index = STEPS.index(r["state"])
        if index == len(STEPS) - 1:
            raise ValueError("Container already left the terminal")
        if r["hold"] and r["state"] == "yard":
            raise ValueError("Customs hold must be cleared before release")
        r["state"] = STEPS[index + 1]
        if r["state"] == "yard":
            r["block"] = "A-01"
        if r["state"] == "gate_out":
            r["departed"] = AS_OF.isoformat()
            r["block"] = "Outside"
    elif p["action"] == "clear_hold":
        if not r["hold"]:
            raise ValueError("No customs hold to clear")
        r["clearance_note"] = text(p, "note", 240)
        r["hold"] = False
    else:
        raise ValueError("Unknown action")
    return r
