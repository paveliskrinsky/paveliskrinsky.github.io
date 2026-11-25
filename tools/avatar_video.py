import sys
from pathlib import Path

import av
from PIL import Image

from images import build

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "avatar.mp4"
OUT = ROOT / "img" / "me"
SIZE = 720
FPS = 30


def poster():
    with av.open(str(SRC)) as c:
        frame = next(c.decode(video=0)).to_image().convert("RGB")
    path = ROOT / "_src" / "me.jpg"
    frame.save(path, quality=95)
    build(path, "me", (1, 1), [160, 480, 800])


def encode(codec, suffix, options):
    target = OUT.with_suffix(suffix)
    with av.open(str(SRC)) as src, av.open(str(target), "w") as dst:
        sin = src.streams.video[0]
        step = max(1, round(float(sin.average_rate) / FPS))
        out = dst.add_stream(codec, rate=FPS)
        out.width = SIZE
        out.height = SIZE
        out.pix_fmt = "yuv420p"
        out.options = options
        n = 0
        for i, frame in enumerate(src.decode(sin)):
            if i % step:
                continue
            img = frame.to_image().resize((SIZE, SIZE), Image.LANCZOS)
            vf = av.VideoFrame.from_image(img).reformat(format="yuv420p")
            vf.pts = n
            n += 1
            for pkt in out.encode(vf):
                dst.mux(pkt)
        for pkt in out.encode():
            dst.mux(pkt)
    print(f"{target.relative_to(ROOT)} {target.stat().st_size // 1024} KB, {n} frames")


def main():
    if not SRC.exists():
        sys.exit(f"no {SRC}")
    poster()
    encode("libx264", ".mp4", {"crf": "26", "preset": "slow", "movflags": "+faststart", "profile": "high"})


if __name__ == "__main__":
    main()
