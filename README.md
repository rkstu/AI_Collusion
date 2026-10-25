# Talk Is Not Collusion

**Do published collusion detectors catch LLM agents that collude on their own?**

Rahul Kumar, Independent Researcher · report: [`paper/paper.pdf`](paper/paper.pdf)

---

Tools that detect collusion between AI agents are usually tested on agents that researchers programmed to hide a secret signal. We ran a published detector suite, unchanged, on language-model sellers in a simulated market who collude without being told to.

Groups of five GPT-4.1 sellers held prices above the competitive level in all 10 sessions, and groups that included two Claude Haiku sellers priced near cost in all 10 matched sessions (p = 0.002, from prices alone). None of the suite's detectors, and no AI judge reading the messages, reliably separated the two markets. The best, the AI judge, ranked a colluding session above a non-colluding one 77% of the time, against 100% for prices, because sellers in both markets used the same kind of collusive language. A simple rule that reads prices instead caught every colluding market within five rounds. Reading the suite's code, we also found that its three comparison methods, reported with perfect scores, are given the list of colluders as an input.

## Verify the results in one command

```bash
python3 verify.py
```

Plain Python, with nothing to install, no API key and no starter kit. It reads the 20 session logs in `runs/` and prints the collusion index for every session, the paired test, the AI judge's scores and ROC AUC, the price rule and the vocabulary count, all in under a second. Every number it prints is in the report.

The detector statistics need the detector suite itself, so `src/analyze.py` recomputes those and draws every figure. Run it from this folder with the starter kit's `steganographic-collusion` environment, setting `STARTER_KIT` to a clone of the kit at `e6fb130`.

```bash
STARTER_KIT=/path/to/collusion_hackathon /path/to/collusion_hackathon/steganographic-collusion/.venv/bin/python src/analyze.py
```

## What we built on, and what we added

Everything here was written and run during the sprint, 23 to 25 October 2026, and none of it is earlier work of ours. The market, the detectors and the monitoring prompt come from published work, used without changing any detector or prompt.

| Component | Source | Ours? |
|---|---|---|
| Market rules, seller instructions, collusion index | Agrawal et al., arXiv:2507.01413, via the starter kit | no |
| Monitoring prompt, used as the AI judge | Agrawal et al., via the starter kit | no |
| Rule-based buyers | Cliff (1997), via the starter kit | no, but we switched their learning back on (patch 02) |
| Collusion detectors and comparison methods | Audit the Whisper, arXiv:2510.04303, via the starter kit | no |
| Fixing each model to one provider | | yes (patch 01, routing only) |
| Two matched markets, scoring only GPT-4.1 sellers, the price rule, analysis, figures, the comparison-method finding | | yes |

The starter kit is [poseidon-research/collusion_hackathon](https://github.com/poseidon-research/collusion_hackathon) at commit `e6fb130`. It is not copied into this repository.

## Where things are

| Folder or file | Contents |
|---|---|
| `paper/` | The report as PDF, the same text as `paper.md` so it reads on GitHub, and the figures |
| `runs/auction/` | Full logs of all 20 sessions, including every price and message |
| `runs/judge/` | The AI judge's score for every round of every session |
| `verify.py` | Recomputes the headline numbers from the logs |
| `src/analyze.py` | Recomputes every number and figure, including the detector statistics |
| `results/` | Every test result and every per-session number behind the figures |
| `docs/PREREG_MAIN.md` | The test plan, written before sessions 5 to 9 were run |
| `patches/` | Our two changes to the starter kit |

## Running the markets again

This needs an OpenRouter key. Clone the starter kit at `e6fb130`, apply the two files in `patches/`, and run from its `llm-agent-collusion/` folder with `PYTHON_DOTENV_DISABLED=1` set. Without that setting, the kit reads any `.env` file in a parent folder, which can route calls to the wrong provider.

## Dual use

The markets are simulated, with no real trades. A result showing that these detectors miss collusion that is not scripted could in principle help someone design agents that avoid them, but the agents here hid nothing and spoke in plain language. The main lesson, to watch outcomes as well as messages, helps defenders, and the code finding concerns evaluation scripts rather than a deployed system.

## Licence and citation

Code is under the MIT License (`LICENSE`). The session logs, judge scores and results are under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). The logs contain text generated through the OpenAI and Anthropic APIs, which those providers' terms allow us to share. The starter kit keeps its own licences.

```
Kumar, R. (2026). Talk Is Not Collusion. Do published collusion detectors catch LLM agents
that collude on their own? https://github.com/rkstu/AI_Collusion
```
