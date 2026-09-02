# Scan-to-CAD — project pointer

Created 2026-09-02. Style reference: `q27b_on_12gb` (one-sentence goal,
scorecard, gates with kill criteria, verdicts written inline, negative
results published). Not the sorting-network contract style.

Authority order:

1. `GOAL_STATE.md` — the goal, scorecard, scope. Frozen by the founder,
   not by an agent.
2. `GATES.md` — decision gates, kill rules, verdict log.
3. Gauntlet manifest (created at Gate 0; frozen thereafter).
4. Implementation convenience — never overrides the above.

Thesis under test: the information destroyed by consumer 3D scanning is
low-entropy — real parts come from a small manifold of design intent
(planes/bores, 0/90/45° angles, round dimensions, standard series,
symmetry) — so a prior-driven pipeline can recover editable parametric
CAD automatically where today a human spends a day.

Non-negotiable rails:

- GAUNTLET-20 is holdout: never tuned on, never trained on, scored at
  most weekly, append-only ledger with commit hashes.
- Every output carries a deviation certificate; one silent
  hallucination fails the part (HON).
- LLMs write programs; only the kernel + scorer make geometry claims.
- A negative reproducible result is completion, not failure.
- Do not modify sibling projects.
