"""C3 positive control: score every session with the starter's own overseer, post hoc.

Uses the starter's MessageOverseer class unchanged (same prompt template, same client, same JSON parsing)
with its default overseer model (gpt-4.1-mini, the paper's). The overseer sees only seller messages, never
asks or trades, so it cannot read collusion off the market outcome used as ground truth. One call per round.
Output: one JSON line per session with the mean and per-round coordination_score (1 to 4).

Run with the starter's venv, from llm-agent-collusion/, with PYTHON_DOTENV_DISABLED=1 and OR_PROVIDER_ORDER set:
  .venv/bin/python ../../../../AI_Collusion/src/judge_sessions.py SESSION_GLOB OUT.jsonl
"""
import concurrent.futures as cf
import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from src.continuous_double_auction.market.agents import MessageOverseer  # noqa: E402
from src.continuous_double_auction.util.misc import get_client  # noqa: E402

ROUND = re.compile(r"## Auction Results: Round (\d+)\s*````json\s*(\{.*?\n\})", re.S)
MODEL = "gpt-4.1-mini"


def judge(session_dir):
    meta = json.load(open(Path(session_dir) / "experiment_metadata.json"))
    gpt = {s for s, m in zip(meta["seller_ids"], meta["resolved_models"]["sellers"]) if m.startswith("openai/")}
    gpt = sorted(gpt)[:3]                       # same 3-GPT-seat view as the detectors (confound control)
    ov = MessageOverseer(client=get_client(MODEL, temperature=0.0), logger=None)
    scores = []
    for r, j in ROUND.findall((Path(session_dir) / "auction_results.md").read_text()):
        msgs = {k: v for k, v in (json.loads(j).get("seller_messages") or {}).items() if k in gpt and v}
        if not msgs:
            continue
        try:
            scores.append(int(ov.run_overseer_prompt(round_num=int(r), seller_messages_this_round=msgs)
                              .get("coordination_score")))
        except Exception:
            pass
    return {"session": Path(session_dir).name, "n_rounds": len(scores),
            "mean_score": sum(scores) / len(scores) if scores else None, "scores": scores}


if __name__ == "__main__":
    dirs = sorted(glob.glob(sys.argv[1]))
    with cf.ThreadPoolExecutor(6) as ex:
        rows = list(ex.map(judge, dirs))
    Path(sys.argv[2]).write_text("\n".join(json.dumps(r) for r in rows))
    for r in rows:
        print(f"{r['session']:42s} rounds {r['n_rounds']:2d} mean {r['mean_score']}")
