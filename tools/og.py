import subprocess
import tempfile

from PIL import Image

from images import OUT, SRC
from previews import BROWSER, BUDGET_MS

SIZE = (1200, 630)


def main():
    page = (SRC / "og.html").resolve().as_uri()
    png = SRC / "og.png"
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([
            BROWSER,
            "--headless=new",
            "--hide-scrollbars",
            "--disable-gpu",
            "--allow-file-access-from-files",
            f"--user-data-dir={profile}",
            f"--window-size={SIZE[0]},{SIZE[1]}",
            f"--virtual-time-budget={BUDGET_MS}",
            f"--screenshot={png}",
            page,
        ], check=True, timeout=120, capture_output=True)
    img = Image.open(png).convert("RGB").crop((0, 0, *SIZE))
    img.save(png, optimize=True)
    dest = OUT / "og.jpg"
    img.save(dest, quality=88, optimize=True, progressive=True)
    print(f"img/og.jpg {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
