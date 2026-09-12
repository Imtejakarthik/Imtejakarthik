from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

OUT = Path("source-prepped.png")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python scripts/prep_photo.py path/to/photo.jpg")

    image = Image.open(sys.argv[1]).convert("RGB")
    width, height = image.size
    left = int(width * 0.23)
    top = int(height * 0.04)
    right = int(width * 0.77)
    bottom = int(height * 0.98)
    image = image.crop((left, top, right, bottom))
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    w, h = image.size
    draw.ellipse((int(w * 0.10), int(h * 0.00), int(w * 0.90), int(h * 0.72)), fill=255)
    draw.rounded_rectangle((int(w * 0.04), int(h * 0.40), int(w * 0.96), int(h * 1.03)), radius=80, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(8))
    image = Image.composite(image, Image.new("RGB", image.size, "white"), mask)
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageEnhance.Contrast(image).enhance(1.85)
    image = ImageEnhance.Sharpness(image).enhance(1.4)
    image.save(OUT)


if __name__ == "__main__":
    main()
