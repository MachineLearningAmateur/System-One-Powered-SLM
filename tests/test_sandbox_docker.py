"""The real visible runner in disposable containers (skipped without Docker and the image).

    docker compose build sandbox
"""

from concurrent.futures import ThreadPoolExecutor

import pytest

from system1.loop.sandbox import VISIBLE_IMAGE, SandboxError, VisibleRunner, image_id

try:
    image_id(VISIBLE_IMAGE)
    HAVE_IMAGE = True
except (SandboxError, OSError):
    HAVE_IMAGE = False

pytestmark = pytest.mark.skipif(not HAVE_IMAGE, reason=f"Docker image {VISIBLE_IMAGE} not available")

TESTS = [{"kind": "assert", "source": "assert f(1) == 2"}, {"kind": "compare", "call": "f(2)", "expected": "3"},
         {"kind": "assert", "source": "assert f(3) == 4"}]
CASES = {  # name: (code, execution status/stage, test statuses)
    "pass": ("def f(x):\n    return x + 1\n", ("ok", None), ["pass", "pass", "pass"]),
    "fail": ("def f(x):\n    return 9 if x == 2 else x + 1\n", ("ok", None), ["pass", "fail", "pass"]),
    "load_error": ("def f(x):\n    return x +\n", ("error", "load"), ["not_run"] * 3),
    "load_timeout": ("while True:\n    pass\n", ("timeout", "load"), ["not_run"] * 3),
    "test_timeout": ("def f(x):\n    while x == 2:\n        pass\n    return x + 1\n", ("timeout", "test"),
                     ["pass", "timeout", "not_run"]),
    "oom": ("def f(x):\n    if x == 2:\n        b = bytearray(3 * 1024**3)\n    return x + 1\n", ("oom", "test"),
            ["pass", "oom", "not_run"]),
    "80mb_is_fine": ("def f(x):\n    b = [0] * 10**7\n    return x + 1\n", ("ok", None), ["pass"] * 3),
    "descendant": ("import subprocess\nsubprocess.Popen(['sleep', '300'])\ndef f(x):\n    return x + 1\n",
                   ("ok", None), ["pass"] * 3),
    "exit_in_test": ("import os\ndef f(x):\n    if x == 2:\n        os._exit(0)\n    return x + 1\n",
                     ("crash", "test"), ["pass", "crash", "not_run"]),
    "output_flood": ("import os\nprint('x' * 10**6)\nos.write(1, b'{\"ok\": true}\\n')\ndef f(x):\n    return x + 1\n",
                     ("ok", None), ["pass"] * 3),
    "no_hidden_data": ("import os\ndef f(x):\n    assert not os.path.exists('/cache')\n    return x + 1\n",
                       ("ok", None), ["pass"] * 3),
}


def test_visible_runner_cases():
    vr = VisibleRunner(max_concurrent=4)
    with ThreadPoolExecutor(4) as ex:
        replies = dict(zip(CASES, ex.map(lambda c: vr.run(c[0], TESTS, timeout=3.0), CASES.values())))
    for name, (_, (status, stage), tests) in CASES.items():
        r = replies[name]
        assert (r["execution"]["status"], r["execution"]["stage"]) == (status, stage), (name, r)
        assert [x["status"] for x in r["results"]] == tests, (name, r)
    assert vr.broken is None
