# -*- coding: utf-8 -*-
"""card.py — the 1200×630 share card: the Golden Triangle, a scrim, the title, Nan's polaroid."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
F = "/System/Library/Fonts/Supplemental/"
W, H = 1200, 630


def main():
    bg = ImageOps.fit(Image.open(ROOT / "docs/img/c/golden-triangle-3.jpg").convert("RGB"), (W, H))
    sc = Image.new("L", (W, 1))
    for x in range(W):
        sc.putpixel((x, 0), int(235 * max(0, 1 - x / 820) ** 1.2 + 40))
    bg = Image.composite(Image.new("RGB", (W, H), (14, 12, 10)), bg, sc.resize((W, H)))
    d = ImageDraw.Draw(bg)
    didot = lambda s, i=0: ImageFont.truetype(F + "Didot.ttc", s, index=i)  # noqa: E731
    sans = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 20, index=0)
    thai = ImageFont.truetype(F + "Tahoma.ttf", 30)
    d.text((64, 70), "PRESENTED WITH LAILA GROUP", font=sans, fill=(224, 180, 88))
    d.text((60, 120), "Chiang Rai,", font=didot(104), fill=(255, 253, 248))
    d.text((60, 232), "Slowly", font=didot(104, 1), fill=(120, 214, 200))
    d.text((64, 370), "Temples in white, blue and black. The Golden Triangle.", font=ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 25), fill=(240, 232, 218))
    d.text((64, 404), "The slow boat to Luang Prabang.", font=ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 25), fill=(240, 232, 218))
    d.text((64, 458), "แอ่วเชียงราย ค่อย ๆ ไปเน้อ", font=thai, fill=(240, 232, 218))
    d.text((64, 560), "hongdam.net · Chiang Rai", font=sans, fill=(200, 190, 175))
    # the polaroid
    p = ImageOps.fit(Image.open(ROOT / "docs/img/own/nan-golden-triangle.jpg").convert("RGB"), (250, 330), centering=(0.5, 0.35))
    frame = Image.new("RGB", (274, 390), (255, 253, 248))
    frame.paste(p, (12, 12))
    ImageDraw.Draw(frame).text((24, 352), "Golden Triangle", font=ImageFont.truetype(F + "Didot.ttc", 24, index=1), fill=(40, 34, 28))
    frame = frame.rotate(4, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
    mask = frame.convert("L").point(lambda v: 255 if v > 3 else 0)
    shadow = Image.new("RGBA", frame.size, (0, 0, 0, 0)); shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.5))
    bg.paste(Image.new("RGB", frame.size, (0, 0, 0)), (870, 132), shadow.split()[3])
    bg.paste(frame, (860, 118), mask)
    bg.save(ROOT / "docs/card.jpg", quality=86, optimize=True)
    print("card", bg.size)


if __name__ == "__main__":
    main()
