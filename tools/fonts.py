import re
import urllib.request
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "fonts"
CSS_URL = "https://fonts.googleapis.com/css2?family=Manrope:wght@500..800&family=Unbounded:wght@500..700&display=swap"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
SUBSETS = ("cyrillic", "latin")
FALLBACK = Path(r"C:\Windows\Fonts\arial.ttf")
SAMPLE = "Быстрые сайты для вашего бизнеса. Сверстаю сайт по макету, сделаю под ключ или ускорю текущий. Fast websites"
WEIGHTS = {"Manrope": 500, "Unbounded": 700}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req) as r:
        return r.read()


def download():
    css = get(CSS_URL).decode()
    faces = []
    for subset, body in re.findall(r"/\* ([\w-]+) \*/\s*@font-face \{(.*?)\}", css, re.S):
        if subset not in SUBSETS:
            continue
        family = re.search(r"font-family: '([^']+)'", body).group(1)
        weight = re.search(r"font-weight: ([\d ]+);", body).group(1)
        url = re.search(r"url\((\S+?)\)", body).group(1)
        urange = re.search(r"unicode-range: ([^;]+);", body).group(1)
        name = f"{family.lower()}-{subset}.woff2"
        OUT.mkdir(exist_ok=True)
        (OUT / name).write_bytes(get(url))
        faces.append((family, weight, name, urange))
    return faces


def width(font, text):
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    return sum(hmtx[cmap[ord(c)]][0] for c in text if ord(c) in cmap) / font["head"].unitsPerEm


def metrics(family):
    files = [OUT / f"{family.lower()}-{s}.woff2" for s in SUBSETS]
    font = TTFont(files[0])
    if "fvar" in font:
        font = instantiateVariableFont(font, {"wght": WEIGHTS[family]})
    latin = TTFont(files[1])
    if "fvar" in latin:
        latin = instantiateVariableFont(latin, {"wght": WEIGHTS[family]})
    fb = TTFont(FALLBACK)
    cyr = "".join(c for c in SAMPLE if ord(c) > 127)
    lat = "".join(c for c in SAMPLE if ord(c) <= 127)
    w = width(font, cyr) + width(latin, lat)
    fw = width(fb, SAMPLE)
    adjust = w / fw
    upm = font["head"].unitsPerEm
    hhea = font["hhea"]
    return {
        "size-adjust": adjust,
        "ascent-override": hhea.ascent / upm / adjust,
        "descent-override": -hhea.descent / upm / adjust,
    }


def main():
    faces = download()
    for family, weight, name, urange in faces:
        print(f"@font-face {{ font-family: '{family}'; font-style: normal; font-weight: {weight}; font-display: swap; "
              f"src: url(fonts/{name}) format('woff2'); unicode-range: {urange}; }}")
    for family in WEIGHTS:
        m = metrics(family)
        print(f"@font-face {{ font-family: '{family} Fallback'; src: local('Arial'); "
              f"size-adjust: {m['size-adjust']:.2%}; ascent-override: {m['ascent-override']:.2%}; "
              f"descent-override: {m['descent-override']:.2%}; line-gap-override: 0%; }}")


if __name__ == "__main__":
    main()
