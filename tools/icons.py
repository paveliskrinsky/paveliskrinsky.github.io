import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "_src" / "logo.jpg"
GRADIENT = ((0x6d, 0x5d, 0xfc), (0x14, 0xc4, 0xa2))
RING = 0.07
SUPERSAMPLE = 4
SVG_PHOTO = 160
ICO_SIZES = [(16, 16), (32, 32), (48, 48)]


def gradient(size):
    (r1, g1, b1), (r2, g2, b2) = GRADIENT
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size - 2)
            px[x, y] = (round(r1 + (r2 - r1) * t), round(g1 + (g2 - g1) * t), round(b1 + (b2 - b1) * t))
    return img


def circle_mask(size, inset=0):
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((inset, inset, size - 1 - inset, size - 1 - inset), fill=255)
    return mask


def ringed(photo, size):
    big = size * SUPERSAMPLE
    out = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    out.paste(gradient(big), (0, 0), circle_mask(big))
    inset = round(big * RING)
    inner = big - 2 * inset
    out.paste(photo.resize((inner, inner), Image.LANCZOS), (inset, inset), circle_mask(inner))
    return out.resize((size, size), Image.LANCZOS)


def save_png(img, dest):
    img.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG).save(dest, optimize=True)


def svg(photo):
    buf = io.BytesIO()
    photo.resize((SVG_PHOTO, SVG_PHOTO), Image.LANCZOS).save(buf, "JPEG", quality=82, optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    (r1, g1, b1), (r2, g2, b2) = GRADIENT
    inset = 64 * RING
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        '  <defs>\n'
        '    <linearGradient id="ring" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">\n'
        f'      <stop offset="0" stop-color="#{r1:02x}{g1:02x}{b1:02x}" />\n'
        f'      <stop offset="1" stop-color="#{r2:02x}{g2:02x}{b2:02x}" />\n'
        '    </linearGradient>\n'
        f'    <clipPath id="face"><circle cx="32" cy="32" r="{32 - inset:g}" /></clipPath>\n'
        '  </defs>\n'
        '  <circle cx="32" cy="32" r="32" fill="url(#ring)" />\n'
        f'  <image x="{inset:g}" y="{inset:g}" width="{64 - 2 * inset:g}" height="{64 - 2 * inset:g}" clip-path="url(#face)" '
        f'href="data:image/jpeg;base64,{data}" />\n'
        '</svg>\n'
    )


def main():
    photo = Image.open(SOURCE).convert("RGB")
    side = min(photo.size)
    photo = photo.crop(((photo.width - side) // 2, (photo.height - side) // 2,
                        (photo.width + side) // 2, (photo.height + side) // 2))

    for name, size in (("icon-192.png", 192), ("icon-512.png", 512)):
        save_png(ringed(photo, size), ROOT / name)
        print(name, size)
    for name, size in (("apple-touch-icon.png", 180), ("icon-maskable-512.png", 512)):
        save_png(photo.resize((size, size), Image.LANCZOS).convert("RGBA"), ROOT / name)
        print(name, size)
    ringed(photo, 256).save(ROOT / "favicon.ico", sizes=ICO_SIZES)
    print("favicon.ico", ICO_SIZES)
    (ROOT / "favicon.svg").write_text(svg(photo), encoding="utf-8")
    print("favicon.svg")


if __name__ == "__main__":
    main()
