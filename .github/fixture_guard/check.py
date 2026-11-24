#!/usr/bin/env python3
"""Tripwire for the intentionally-seeded test fixtures.

Each sentinel is the SHA-256 of one stripped source line. The check fails if
any sentinel no longer appears in a tracked Python file, i.e. a fixture line was
removed or rewritten (for example by a merged remediation PR).

    check.py                  verify (exit 1 on any missing sentinel)
    check.py --add FILE:LINE  add the hash of that line to sentinels.json
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SENTINELS = Path(__file__).with_name("sentinels.json")


def h(line: str) -> str:
    return hashlib.sha256(line.strip().encode()).hexdigest()


def tracked_py() -> list[str]:
    out = subprocess.check_output(["git", "ls-files", "*.py"], text=True)
    return out.splitlines()


def main() -> int:
    data = json.loads(SENTINELS.read_text())
    if len(sys.argv) == 3 and sys.argv[1] == "--add":
        path, lineno = sys.argv[2].rsplit(":", 1)
        line = Path(path).read_text().splitlines()[int(lineno) - 1]
        data["hashes"] = sorted(set(data["hashes"]) | {h(line)})
        SENTINELS.write_text(json.dumps(data, indent=1) + "\n")
        print("added; total", len(data["hashes"]))
        return 0

    seen = set()
    for f in tracked_py():
        try:
            seen.update(h(x) for x in Path(f).read_text(encoding="utf-8").splitlines())
        except (OSError, UnicodeDecodeError):
            continue
    missing = [i for i, x in enumerate(data["hashes"]) if x not in seen]
    if missing:
        print(f"FIXTURE GUARD FAILED: {len(missing)}/{len(data['hashes'])} sentinels missing (indexes {missing})")
        return 1
    print(f"fixture guard ok: {len(data['hashes'])}/{len(data['hashes'])} sentinels present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
