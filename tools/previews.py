import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

from images import SRC, PROJECT_WIDTHS, build

SITES = {
    "kemvod": "https://kemvod.ru",
    "zelzoo": "https://test.zelzoo.ru",
    "vvezi": "https://vvezi.ru",
    "autoparam": "https://autoparam.ru",
    "kodrazbor": "https://kodrazbor.ru",
}
BROWSER = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
VIEWPORT = (1440, 900)
CROP_HEIGHT = 768
BUDGET_MS = 15000


def shoot(url, dest):
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([
            BROWSER,
            "--headless=new",
            "--hide-scrollbars",
            "--disable-gpu",
            f"--user-data-dir={profile}",
            f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}",
            f"--virtual-time-budget={BUDGET_MS}",
            f"--screenshot={dest}",
            url,
        ], check=True, timeout=120, capture_output=True)


def main():
    names = sys.argv[1:] or list(SITES)
    (SRC / "projects").mkdir(parents=True, exist_ok=True)
    for name in names:
        png = SRC / "projects" / f"{name}.png"
        shoot(SITES[name], str(png))
        img = Image.open(png).convert("RGB")
        img.crop((0, 0, VIEWPORT[0], CROP_HEIGHT)).save(png, optimize=True)
        build(f"projects/{name}.png", f"projects/{name}", None, PROJECT_WIDTHS)


if __name__ == "__main__":
    main()
