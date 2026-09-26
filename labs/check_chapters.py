"""Execute the textbook's Python examples and their behavioral checks.

Only run trusted authored chapters: this executes code, not untrusted captions.
No third-party packages or model services are required by the examples.
"""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import argparse
import json
import re
import math

ROOT = Path(__file__).resolve().parents[1]


def run(chapter):
    source = (ROOT / f"chapters/lecture-{chapter:02d}.md").read_text(
        encoding="utf-8"
    )
    blocks = re.findall(r"```python\n(.*?)```", source, re.S)
    if not blocks:
        raise AssertionError(f"Chapter {chapter} has no executable example")
    namespace = {"__name__": "chapter_example"}
    output = StringIO()
    with redirect_stdout(output):
        for index, block in enumerate(blocks):
            filename = f"lecture-{chapter:02d}:block-{index + 1}"
            exec(compile(block, filename, "exec"), namespace)
    invalid_cases = {
        1: ("workload_value", (10, 1.1, 2, 0.1)),
        2: ("excess_loss", (0, 10)),
        3: ("deficit_hours", ([(1, 1.2)],)),
        4: ("checkpoint_plan", (0, 100)),
        5: ("verified_path_probability", (0.9, -0.1, 0.9)),
        6: ("roofline", (100, 0, 1)),
        7: ("storage_required", (120, 12, 0, 0.9)),
        8: ("network_gross_value", (2.5, 0.1, 100)),
        9: ("difference_interval", (0.5, 10, 2, 10)),
        10: ("rollout_bound", (1.1, 0.01, -1)),
        11: ("euler_exp", (0,)),
        12: ("first_audio_ms", (0, 0, 0, -1, 0, 0)),
    }
    if chapter in invalid_cases:
        name, arguments = invalid_cases[chapter]
        try:
            namespace[name](*arguments)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{name} accepted invalid inputs")
    if chapter == 9:
        interval = namespace["difference_interval"]
        estimate, lower, upper = interval(400, 1000, 440, 1000)
        assert math.isclose(estimate, 0.04)
        assert lower < 0 < upper
        reversed_result = interval(440, 1000, 400, 1000)
        assert math.isclose(reversed_result[1], -upper)
        try:
            interval(2, 1, 0, 10)
        except ValueError:
            pass
        else:
            raise AssertionError("Impossible counts were accepted")
    return {"chapter": chapter, "blocks": len(blocks),
            "output": output.getvalue().strip(), "checks": "passed"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapter", nargs="?", type=int)
    args = parser.parse_args()
    if args.chapter is not None and not 1 <= args.chapter <= 13:
        parser.error("Chapter must be between 1 and 13")
    chapters = [args.chapter] if args.chapter else range(1, 14)
    results = [run(chapter) for chapter in chapters]
    if args.chapter is None:
        (ROOT / "validation").mkdir(exist_ok=True)
        (ROOT / "validation/lab-checks.json").write_text(
            json.dumps(results, indent=2), encoding="utf-8"
        )
    print(json.dumps(results, indent=2))
