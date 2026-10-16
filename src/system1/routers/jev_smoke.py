"""One small billed Jev call: checks the key, the response shape and usage.

The client validates the response (ids, probabilities, sums, usage, model
version), so a call that returns is a valid call. These questions only test
the transport; they are not the frozen experimental rubric.

Run with:  uv run jev-smoke
"""

from __future__ import annotations

import json
import sys

from system1.config import RESULTS, load_prices
from system1.eval.ledger import CostLedger
from system1.routers.jev import JevClient, JevProtocolError, JevRequestError

STATE = {
    "task": "Write add(a, b) that returns the sum of two integers.",
    "code": "def add(a, b):\n    return a - b\n",
    "visible_test_output": "assert add(2, 3) == 5  ->  AssertionError: -1 != 5",
    "thinking": "I need to add the numbers. I wrote a - b. The test expects 5 but got -1. "
    "Maybe the test itself is wrong, so I will keep the code.",
}

QUESTIONS = {
    "on_task": {
        "type": "noul",
        "instructions": "Is the model still working on the assigned task?",
    },
    "unsupported_claim": {
        "type": "noul",
        "instructions": "Does the thinking make a claim about the code or the tests "
        "that the supplied evidence does not support?",
    },
    "status": {
        "type": "choice",
        "instructions": "Is the model on track, or is it drifting, lost or hallucinating?",
        "criteria": {
            "on_track": "The reasoning follows the task and the test feedback.",
            "drifting": "The reasoning ignores or misreads the feedback, or is lost.",
        },
    },
}


def main() -> int:
    ledger = CostLedger(RESULTS / "jev_smoke_ledger.jsonl")
    try:
        with JevClient(ledger=ledger, prices=load_prices()) as jev:
            r = jev.ask(STATE, QUESTIONS, task_id="smoke/add", attempt=0, step=1, arm="base+trace")
    except (JevProtocolError, JevRequestError) as e:
        print(f"FAILED: {e}")
        print(f"ledger rows    : {ledger.path}")
        return 1

    print(f"model returned : {r.model_returned}")
    print(f"tokens in/out  : {r.input_tokens} / {r.output_tokens}")
    print(f"latency        : {r.latency_ms:.0f} ms over {r.http_attempts} HTTP attempt(s)")
    print(f"request bytes  : {r.request_bytes} (exact bytes sent)")
    print("answers        :")
    print(json.dumps(r.answers, indent=2))
    print("checks         : response passed validation")
    print(f"ledger rows    : {ledger.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
