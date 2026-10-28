import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

from images import SRC, PROJECT_WIDTHS, build

SITES = {
    "kemvod": "https://kemvod.ru",
    "zelzoo": "https://zelzoo.ru",
    "vvezi": "https://vvezi.ru",
    "zaveli": "https://zaveli.ru",
    "kodrazbor": "https://kodrazbor.ru",
    "kombos": "https://kombos.ru",
}
BROWSER = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
VIEWPORT = (1440, 2000)
CROP_HEIGHT = 1800
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


def changed(name):
    old = SRC / "projects" / f"{name}.png"
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / f"{name}.png"
        shoot(SITES[name], str(fresh))
        new = Image.open(fresh).convert("RGB").crop((0, 0, VIEWPORT[0], CROP_HEIGHT))
        if not old.exists():
            return True
        prev = Image.open(old).convert("RGB")
        if prev.size != new.size:
            return True
        return ImageChops.difference(prev, new).getbbox() is not None


def main():
    args = sys.argv[1:]
    if args[:1] == ["--changed"]:
        names = [n for n in (args[1:] or list(SITES)) if changed(n)]
        print("changed:", ", ".join(names) or "none")
    else:
        names = args or list(SITES)
    (SRC / "projects").mkdir(parents=True, exist_ok=True)
    for name in names:
        png = SRC / "projects" / f"{name}.png"
        shoot(SITES[name], str(png))
        img = Image.open(png).convert("RGB")
        img.crop((0, 0, VIEWPORT[0], CROP_HEIGHT)).save(png, optimize=True)
        build(f"projects/{name}.png", f"projects/{name}", None, PROJECT_WIDTHS)


if __name__ == "__main__":
    main()
