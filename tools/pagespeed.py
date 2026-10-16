import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from previews import BROWSER, SITES

CATEGORIES = ["performance", "accessibility", "best-practices", "seo"]
PRESETS = ["mobile", "desktop"]


def run(url, preset):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.json"
        cmd = [
            "npx", "--yes", "lighthouse@12", url,
            "--quiet", "--output=json", f"--output-path={out}",
            f"--only-categories={','.join(CATEGORIES)}",
            "--chrome-flags=--headless=new",
        ]
        if preset == "desktop":
            cmd.append("--preset=desktop")
        proc = subprocess.run(cmd, timeout=300, capture_output=True, text=True, shell=os.name == "nt",
                              env={**os.environ, "CHROME_PATH": BROWSER})
        if not out.exists():
            raise RuntimeError(proc.stderr.strip().splitlines()[-1] if proc.stderr else proc.returncode)
        cats = json.loads(out.read_text(encoding="utf-8"))["categories"]
    return {c: round(cats[c]["score"] * 100) for c in CATEGORIES}


def main():
    names = sys.argv[1:] or list(SITES)
    for name in names:
        for preset in PRESETS:
            try:
                scores = run(SITES[name], preset)
                print(name, preset, " ".join(f"{k}={v}" for k, v in scores.items()), flush=True)
            except Exception as e:
                print(name, preset, "error", e, flush=True)


if __name__ == "__main__":
    main()
