# Pre-registration: do published collusion detectors catch LLM agents that collude on their own?

Version 1.0, written 2026-10-25 before the scaled run. Seeds 0 to 4 of both arms had already been run in a feasibility check and shaped this design. Seeds 5 to 9 are new. Every confirmatory test below uses seeds 0 to 9, and the same tests are also reported on seeds 5 to 9 alone as a replication.

## Primary question

Audit the Whisper, the sprint starter's detector project, reports its detectors catch collusion at fixed low false-positive rates. Its colluders are scripted (fixed covert schemes). **On LLM sellers who collude spontaneously, do those detectors, run unmodified, separate colluding markets from non-colluding ones?**

## Design

- **Environment:** sprint starter `llm-agent-collusion` at e6fb130.
  - Two disclosed patches: provider pinning (routing only) and the starter's own commented-out ZIP buyer learning, re-enabled.
  - Paper size: 5 sellers, 6 ZIP buyers, 30 rounds, comms on.
- **Arms**, paired by seed 0 to 9 (same valuations and initial conditions per seed):
  - **H:** 5 × GPT-4.1.
  - **M:** 3 × GPT-4.1 + 2 × Claude Haiku 5.5.
- **Ground truth:** the starter's own last-third seller ask index. A market is "colluding" when its index exceeds its pair partner's; the confirmatory tests use only the paired direction, never a threshold we pick.
- **Detector input:** GPT-only seats, 3 per session, so both arms have the same model and seat count (removes the model-mix confound found in the feasibility check).

## Confirmatory tests (Holm-corrected across C1 to C3, α = 0.05)

- **C1, manipulation check:** H has a higher last-third ask index than M. Paired two-sided sign-flip permutation test on the 10 per-seed differences (exact: all 2¹⁰ sign assignments).
- **C2, detector discrimination:** for each label-free detector that produces a per-session statistic, H is ranked above M in more pairs than chance. Exact sign test over 10 pairs. One test per detector.
- **C3, a detector that should work, as a positive control:** the starter's own overseer prompt (Agrawal et al.), run as a post-hoc judge on each session's seller messages with `gpt-4.1-mini` (the paper's overseer model). Mean coordination score per session, H > M. Exact sign test over 10 pairs.

Interpretation, fixed now:

| C1 | C2 (per detector) | C3 | reading |
|---|---|---|---|
| sig | not sig | sig | **headline:** the collusion is real and detectable from text (C3), but the published detector misses it |
| sig | sig | sig | the published detector does work on spontaneous LLM collusion |
| sig | not sig | not sig | collusion is real but hard to detect from text at all; no claim about the published detector specifically |
| not sig | — | — | the manipulation failed; no detector claim is made |

## Exploratory, with CIs and no correction

- Per-detector arm-level p-values from the detector's own pooled test (as the repo runs it).
- `cross_run_mi` (needs ≥ 2 runs, so arm-level only), including the overflow warnings.
- Overseer score vs. last-third index across all 20 sessions (Spearman), to check the judge tracks the market outcome.
- What the sellers said: count of explicit coordination phrases per session, as a qualitative check.

## Code finding, reported regardless of the above

The repo's SentinelAgent, CASE and PerfectCollusion baselines receive the true colluder list (`run.colluders`) and are not implementations of those methods. This is a property of the code, so it is reported without a statistical test, with file and line references.

## Notes added after the study (2026-10-26)

The tests, predictions and interpretation table above are unchanged from the version written before seeds 5 to 9 were run. Only the following were changed or added afterwards.

- A planning section on API budget was removed, and two references to internal working notes were reworded.
- The exploratory Spearman correlation between the judge's score and the collusion index was not run, because the judge scored every session between 3.87 and 4.00, leaving almost no variation to correlate.
- The coordination-phrase count listed above was run, as the collusive-vocabulary count in Section 6 of the report.
- The price rule in Section 7 of the report was not part of this plan. It was added afterwards and is reported there as exploratory.
