export function inspect(r) {
  const next = {
    arrived: "Move to yard",
    yard: "Release container",
    released: "Record gate out",
  };
  return {
    fields: [
      ["Vessel", r.vessel],
      ["Equipment", `${r.teu === 2 ? "40" : "20"} ft · ${r.teu} TEU`],
      ["Arrival · UTC", r.arrived],
      ["Customs", r.hold ? "Hold active" : "Clear"],
      [
        "Dwell exception",
        r.state === "gate_out"
          ? "No active exception · journey complete"
          : r.exception
            ? "Above 5-day target"
            : "Within target",
      ],
      ["Current block", r.block],
    ],
    forms: [
      ...(r.hold
        ? [
            {
              title: "Customs clearance",
              help: "Simulation only: record the reason for clearing this hold.",
              action: "clear_hold",
              button: "Clear customs hold",
              fields: [
                {
                  key: "note",
                  label: "Clearance reference / reason",
                  type: "textarea",
                  maxLength: 240,
                },
              ],
            },
          ]
        : []),
      ...(next[r.state]
        ? [
            {
              title: "Next milestone",
              action: "advance",
              button: next[r.state],
              help:
                r.hold && r.state === "yard"
                  ? "The customs hold must be cleared before release."
                  : "The state transition and audit entry are saved together.",
              fields: [],
            },
          ]
        : []),
    ],
    note:
      r.state === "gate_out"
        ? "Journey complete. Dwell is frozen at the recorded gate-out time."
        : "The simulation clock is fixed for reproducible dwell metrics.",
  };
}
