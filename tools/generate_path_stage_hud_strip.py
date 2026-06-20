from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "assets" / "system" / "path-stage-hud-strip-20260618.png"


def main() -> None:
    random.seed(20260618)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    width, height = 1792, 512
    image = Image.new("RGB", (width, height), (5, 7, 8))
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            nx = x / (width - 1)
            ny = y / (height - 1)
            vignette = 1 - min(0.75, ((nx - 0.5) ** 2 * 1.8 + (ny - 0.5) ** 2 * 3.2))
            scan = 8 * math.sin((x * 0.018) + (y * 0.055)) + 5 * math.sin(
                (x * 0.006) - (y * 0.031)
            )
            red = int((6 + 14 * vignette + scan * 0.20) * (1 - ny * 0.18))
            green = int(10 + 24 * vignette + scan * 0.28)
            blue = int(12 + 22 * vignette + scan * 0.35)
            pixels[x, y] = (
                max(0, min(255, red)),
                max(0, min(255, green)),
                max(0, min(255, blue)),
            )

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    for x in range(0, width, 56):
        alpha = 18 if x % 224 else 42
        draw.line([(x, 0), (x, height)], fill=(76, 216, 205, alpha), width=1)
    for y in range(24, height, 48):
        alpha = 13 if y % 192 else 34
        draw.line([(0, y), (width, y)], fill=(245, 185, 86, alpha), width=1)

    for i in range(-4, 9):
        y0 = int(height * 0.58 + i * 38)
        draw.line([(0, y0), (width, y0 - 180)], fill=(64, 210, 190, 28), width=2)
        draw.line([(0, y0 + 18), (width, y0 - 162)], fill=(251, 120, 88, 13), width=1)

    for inset, alpha in [(0, 44), (46, 24), (96, 14)]:
        draw.rounded_rectangle(
            [96 + inset, 102 + inset // 4, width - 96 - inset, height - 102 - inset // 4],
            radius=44,
            fill=(3, 6, 7, alpha),
        )

    rail_y = int(height * 0.50)
    for radius, alpha in [(64, 18), (42, 28), (28, 44), (14, 76), (5, 190)]:
        draw.rounded_rectangle(
            [72, rail_y - radius, width - 72, rail_y + radius],
            radius=radius,
            outline=(66, 224, 208, alpha),
            width=max(1, radius // 9),
        )

    for i in range(9):
        x = int(126 + i * ((width - 252) / 8))
        if i % 4 == 0:
            primary, secondary = (72, 231, 204), (244, 186, 72)
        elif i % 4 == 1:
            primary, secondary = (90, 225, 145), (72, 231, 204)
        elif i % 4 == 2:
            primary, secondary = (242, 126, 92), (244, 186, 72)
        else:
            primary, secondary = (112, 138, 146), (72, 231, 204)

        for radius, alpha in [(72, 20), (52, 36), (34, 62), (21, 104)]:
            draw.ellipse(
                [x - radius, rail_y - radius, x + radius, rail_y + radius],
                outline=(*primary, alpha),
                width=2,
            )
        draw.rounded_rectangle(
            [x - 28, rail_y - 6, x + 28, rail_y + 6],
            radius=6,
            fill=(*primary, 30),
        )
        draw.ellipse(
            [x - 10, rail_y - 10, x + 10, rail_y + 10],
            fill=(*secondary, 180),
            outline=(255, 248, 202, 150),
            width=2,
        )
        draw.arc(
            [x - 31, rail_y - 31, x + 31, rail_y + 31],
            start=25 + i * 13,
            end=215 + i * 13,
            fill=(*secondary, 140),
            width=4,
        )

        for j in range(6):
            angle = (j / 6) * math.tau + i * 0.17
            radius = 52 + random.randint(-8, 10)
            px = x + math.cos(angle) * radius
            py = rail_y + math.sin(angle) * radius * 0.55
            draw.line([(px - 5, py), (px + 5, py)], fill=(*secondary, 88), width=1)
            draw.line([(px, py - 5), (px, py + 5)], fill=(*primary, 66), width=1)

    for _ in range(80):
        x = random.randrange(40, width - 120)
        y = random.randrange(46, height - 72)
        block_width = random.randrange(18, 96)
        block_height = random.randrange(2, 7)
        color = random.choice(
            [(73, 225, 203), (243, 184, 79), (247, 119, 90), (82, 221, 142)]
        )
        draw.rounded_rectangle(
            [x, y, x + block_width, y + block_height],
            radius=block_height // 2,
            fill=(*color, random.randrange(18, 56)),
        )

    for i, x in enumerate([260, 615, 1030, 1445]):
        draw.polygon(
            [(x - 120, 0), (x - 52, 0), (x + 155, height), (x + 66, height)],
            fill=(68, 222, 205, 18 if i != 2 else 28),
        )
        draw.polygon(
            [(x + 18, 0), (x + 47, 0), (x + 232, height), (x + 185, height)],
            fill=(248, 180, 72, 10),
        )

    for y, alpha in [(22, 90), (34, 34), (height - 24, 86), (height - 38, 30)]:
        draw.line([(64, y), (width - 64, y)], fill=(214, 239, 221, alpha), width=1)
    for x in [88, width - 88]:
        draw.rounded_rectangle(
            [x - 18, 72, x + 18, height - 72],
            radius=14,
            outline=(245, 185, 86, 72),
            width=2,
        )

    image = Image.alpha_composite(image.convert("RGBA"), overlay.filter(ImageFilter.GaussianBlur(0.35)))
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = pixels[x, y]
            noise = random.randint(-5, 5)
            pixels[x, y] = (
                max(0, min(255, red + noise)),
                max(0, min(255, green + noise)),
                max(0, min(255, blue + noise)),
                alpha,
            )

    image.save(OUT, optimize=True)
    print(f"{OUT} {OUT.stat().st_size}")


if __name__ == "__main__":
    main()
