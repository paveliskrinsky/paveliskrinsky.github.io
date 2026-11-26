from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public_html"
ARCHIVE = ROOT / "public_html.zip"
PUBLIC_FILES = (
    "index.html", "ai-services.html", "privacy.html", "404.html",
    "page.css", "ai-services.css", "ai-services.js",
    "robots.txt", "sitemap.xml", "site.webmanifest",
    "favicon.ico", "favicon.svg", "apple-touch-icon.png",
    "icon-192.png", "icon-512.png", "icon-maskable-512.png",
)
ASSET_TYPES = {
    "fonts": {".woff2"},
    "img": {".jpg", ".webp", ".avif", ".png", ".svg", ".mp4"},
}


def public_files():
    for name in PUBLIC_FILES:
        yield ROOT / name
    for directory, extensions in ASSET_TYPES.items():
        for asset in sorted((ROOT / directory).rglob("*")):
            if asset.is_file() and asset.suffix.lower() in extensions:
                yield asset


def main():
    with TemporaryDirectory(dir=ROOT) as temporary:
        staging = Path(temporary)
        site = staging / OUTPUT.name
        archive = staging / ARCHIVE.name
        with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
            for source in public_files():
                target = site / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                copy2(source, target)
                bundle.write(target, target.relative_to(staging))
        with ZipFile(archive) as bundle:
            if bundle.testzip() is not None:
                raise ValueError("ZIP verification failed")
            count = len(bundle.namelist())

        previous = staging / "previous"
        if OUTPUT.exists():
            OUTPUT.rename(previous)
        try:
            site.rename(OUTPUT)
            try:
                archive.replace(ARCHIVE)
            except OSError:
                OUTPUT.rename(site)
                raise
        except OSError:
            if previous.exists():
                previous.rename(OUTPUT)
            raise

    print(f"{ARCHIVE.name}: {count} files, {ARCHIVE.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
