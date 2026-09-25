"""Generate the link-preview card and favicons.

Run from the repo root:  uv run --with pillow python tools/make_images.py
Edit the text below when the headline or focus changes.
"""
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

NAME = "Julian Fritsch"
LOCATION = "LAUSANNE, SWITZERLAND"
HEADLINE = ("Machine Learning Engineer | PhD", "Production AI & MLOps")
FOCUS = "ML engineering · forward-deployed engineering · AI in health"
URL = "jufrit.github.io"
SECTIONS = "Experience · Publications · CV"

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path(__file__).resolve().parent / ".fonts"
FONTS = {
    "sans": "https://github.com/google/fonts/raw/main/ofl/googlesansflex/GoogleSansFlex%5BGRAD,ROND,opsz,slnt,wdth,wght%5D.ttf",
    "mono": "https://github.com/google/fonts/raw/main/ofl/googlesanscode/GoogleSansCode%5Bwght%5D.ttf",
}
FG, MUTED, RULE, BG = (31, 31, 31), (95, 99, 104), (227, 227, 227), (255, 255, 255)
S = 2  # render at 2x, downscale for smooth edges


def font_path(kind):
    path = FONT_DIR / f"{kind}.ttf"
    if not path.exists():
        FONT_DIR.mkdir(exist_ok=True)
        urllib.request.urlretrieve(FONTS[kind], path)
    return path


def sans(size, weight=400):
    f = ImageFont.truetype(font_path("sans"), size)
    f.set_variation_by_axes([weight if a["name"] in (b"Weight", "Weight") else a["default"]
                             for a in f.get_variation_axes()])
    return f


def mono(size):
    f = ImageFont.truetype(font_path("mono"), size)
    f.set_variation_by_axes([400])
    return f


def card():
    W, H, PAD = 1200 * S, 627 * S, 80 * S
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    ps = 250 * S
    photo = Image.open(ROOT / "data/photoGM.jpeg").convert("RGB").resize((ps, ps), Image.LANCZOS)
    mask = Image.new("L", (ps, ps), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, ps - 1, ps - 1), radius=32 * S, fill=255)
    img.paste(photo, (W - PAD - ps, PAD), mask)

    x, y = PAD, PAD
    d.text((x, y), LOCATION, font=mono(20 * S), fill=MUTED)
    y += 56 * S
    d.text((x, y), NAME, font=sans(72 * S, 500), fill=FG)
    y += 110 * S
    for line in HEADLINE:
        d.text((x, y), line, font=sans(36 * S), fill=FG)
        y += 50 * S
    y += 18 * S
    d.text((x, y), FOCUS, font=sans(24 * S), fill=MUTED)

    fy = H - PAD - 24 * S
    d.line((PAD, fy - 28 * S, W - PAD, fy - 28 * S), fill=RULE, width=2 * S)
    d.text((PAD, fy), URL, font=mono(22 * S), fill=FG)
    f = sans(22 * S)
    d.text((W - PAD - d.textlength(SECTIONS, font=f), fy), SECTIONS, font=f, fill=MUTED)

    img.resize((W // S, H // S), Image.LANCZOS).save(ROOT / "data/social-card.png", optimize=True)


def icon(size):
    big = size * 8
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, big - 1, big - 1), radius=big // 5, fill=FG)
    d.text((big / 2, big / 2), "JF", font=sans(int(big * 0.5), 500), fill=BG, anchor="mm")
    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    card()
    icon(256).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    icon(180).save(ROOT / "apple-touch-icon.png")
