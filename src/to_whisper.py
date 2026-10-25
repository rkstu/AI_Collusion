"""Convert one llm-agent-collusion session into an Audit-the-Whisper transcript (JSONL).

Each seller-round becomes {"run_id", "round_id", "agent_id", "role", "message", "action"}, the format
the auditor's FeatureExtractor reads. Seller names differ between sessions, so sellers are mapped to
stable seat roles seller_1..seller_N by their order in round 1 (the MI detector pairs roles across runs).
The message keeps the seller's own text and appends "Ask:<ask>" so price features are populated.

  python3 -I src/to_whisper.py SESSION_DIR OUT.jsonl
"""
import json
import re
import sys
from pathlib import Path

ROUND = re.compile(r"## Auction Results: Round (\d+)\s*````json\s*(\{.*?\n\})", re.S)


def convert(session_dir, out_path):
    text = (Path(session_dir) / "auction_results.md").read_text()
    rounds = [(int(r), json.loads(j)) for r, j in ROUND.findall(text)]
    if not rounds:
        raise SystemExit(f"no rounds parsed in {session_dir}")
    seats = {name: f"seller_{i + 1}" for i, name in enumerate(rounds[0][1]["seller_asks"])}
    run_id = Path(session_dir).name
    with open(out_path, "w") as f:
        for r, d in rounds:
            for name, ask in d["seller_asks"].items():
                msg = (d.get("seller_messages") or {}).get(name) or ""
                f.write(json.dumps({"run_id": run_id, "round_id": r, "agent_id": seats[name], "role": seats[name],
                                    "message": f"{msg} Ask:{ask}".strip(), "action": str(ask)}) + "\n")
    return len(rounds), len(seats)


if __name__ == "__main__":
    n_rounds, n_seats = convert(sys.argv[1], sys.argv[2])
    print(f"{sys.argv[1]}: {n_rounds} rounds x {n_seats} sellers -> {sys.argv[2]}")
