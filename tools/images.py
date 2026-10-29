import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
OUT = ROOT / "img"

JOBS = [
    ("avatar.jpg", "avatar", (3, 4), [160, 480, 560, 800], 45),
    ("logo.jpg", "logo", (1, 1), [96], 55),
]
PROJECT_WIDTHS = [520, 640, 1200]


def jobs():
    yield from JOBS
    for png in sorted((SRC / "projects").glob("*.png")):
        yield f"projects/{png.name}", f"projects/{png.stem}", None, PROJECT_WIDTHS, 55


def crop_to(img, ratio):
    if not ratio:
        return img
    w, h = img.size
    rw, rh = ratio
    if w * rh > h * rw:
        nw = h * rw // rh
        return img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    return img.crop((0, 0, w, w * rh // rw))


def build(src, name, ratio, widths, avif_quality=55):
    img = crop_to(ImageOps.exif_transpose(Image.open(SRC / src)).convert("RGB"), ratio)
    dest = OUT / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    for w in widths:
        h = round(img.height * w / img.width)
        out = img.resize((w, h), Image.LANCZOS)
        base = f"{dest}-{w}"
        out.save(f"{base}.avif", "AVIF", quality=avif_quality, speed=4)
        out.save(f"{base}.webp", "WEBP", quality=78, method=6)
        out.save(f"{base}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
        sizes = [Path(f"{base}.{e}").stat().st_size // 1024 for e in ("avif", "webp", "jpg")]
        print(f"{name}-{w} {w}x{h} avif/webp/jpg KB: {sizes}")


def main():
    only = set(sys.argv[1:])
    for job in jobs():
        if not only or job[1] in only:
            build(*job)


if __name__ == "__main__":
    main()
