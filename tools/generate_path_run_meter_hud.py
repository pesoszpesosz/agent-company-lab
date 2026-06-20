from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "assets" / "system" / "path-run-meter-hud-20260618.png"


def main() -> None:
    random.seed(20260618 + 17)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    width, height = 1408, 384
    image = Image.new("RGB", (width, height), (4, 7, 8))
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            nx = x / (width - 1)
            ny = y / (height - 1)
            rail_glow = math.exp(-((ny - 0.5) ** 2) * 22)
            vignette = 1 - min(0.82, ((nx - 0.5) ** 2 * 1.6 + (ny - 0.5) ** 2 * 2.4))
            scan = 5 * math.sin(x * 0.025 + y * 0.036) + 4 * math.sin(x * 0.008 - y * 0.045)
            pixels[x, y] = (
                max(0, min(255, int(5 + 14 * vignette + 4 * rail_glow + scan * 0.18))),
                max(0, min(255, int(10 + 25 * vignette + 18 * rail_glow + scan * 0.25))),
                max(0, min(255, int(12 + 24 * vignette + 20 * rail_glow + scan * 0.32))),
            )

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    for x in range(0, width, 44):
        alpha = 14 if x % 176 else 34
        draw.line([(x, 0), (x, height)], fill=(64, 218, 204, alpha), width=1)
    for y in range(18, height, 34):
        alpha = 10 if y % 136 else 28
        draw.line([(0, y), (width, y)], fill=(244, 186, 85, alpha), width=1)

    rail_y = int(height * 0.5)
    draw.rounded_rectangle([54, rail_y - 86, width - 54, rail_y + 86], radius=86, fill=(0, 0, 0, 58))
    for radius, alpha in [(76, 18), (52, 34), (28, 60), (8, 132)]:
        draw.rounded_rectangle(
            [86, rail_y - radius, width - 86, rail_y + radius],
            radius=radius,
            outline=(68, 230, 205, alpha),
            width=max(1, radius // 12),
        )

    socket_count = 5
    for index in range(socket_count):
        x = int(142 + index * ((width - 284) / (socket_count - 1)))
        if index == 1:
            primary, secondary = (248, 112, 92), (244, 186, 85)
        elif index in (2, 4):
            primary, secondary = (110, 226, 136), (68, 230, 205)
        else:
            primary, secondary = (68, 230, 205), (244, 186, 85)

        for radius, alpha in [(92, 14), (64, 26), (42, 50), (25, 88)]:
            draw.ellipse(
                [x - radius, rail_y - radius, x + radius, rail_y + radius],
                outline=(*primary, alpha),
                width=2,
            )
        draw.rounded_rectangle(
            [x - 88, rail_y - 28, x + 88, rail_y + 28],
            radius=24,
            fill=(2, 6, 8, 132),
            outline=(*primary, 58),
            width=2,
        )
        draw.ellipse(
            [x - 18, rail_y - 18, x + 18, rail_y + 18],
            fill=(*secondary, 178),
            outline=(255, 246, 204, 128),
            width=2,
        )
        draw.arc(
            [x - 43, rail_y - 43, x + 43, rail_y + 43],
            start=30 + index * 24,
            end=224 + index * 24,
            fill=(*secondary, 138),
            width=4,
        )

        for spark in range(8):
            angle = (spark / 8) * math.tau + index * 0.3
            px = x + math.cos(angle) * random.randrange(52, 78)
            py = rail_y + math.sin(angle) * random.randrange(24, 48)
            draw.line([(px - 5, py), (px + 5, py)], fill=(*secondary, 76), width=1)
            draw.line([(px, py - 5), (px, py + 5)], fill=(*primary, 58), width=1)

    for _ in range(140):
        x = random.randrange(44, width - 44)
        y = random.randrange(34, height - 34)
        block_width = random.randrange(12, 70)
        block_height = random.randrange(2, 5)
        color = random.choice(
            [(68, 230, 205), (244, 186, 85), (248, 112, 92), (110, 226, 136)]
        )
        draw.rounded_rectangle(
            [x, y, x + block_width, y + block_height],
            radius=block_height // 2,
            fill=(*color, random.randrange(16, 48)),
        )

    for x, alpha in [(102, 70), (width - 102, 70), (width // 2, 32)]:
        draw.rounded_rectangle(
            [x - 15, 48, x + 15, height - 48],
            radius=14,
            outline=(244, 186, 85, alpha),
            width=2,
        )

    for x in [260, 580, 920, 1220]:
        draw.polygon(
            [(x - 72, 0), (x - 36, 0), (x + 95, height), (x + 48, height)],
            fill=(68, 230, 205, 16),
        )

    for y, alpha in [(20, 82), (32, 28), (height - 20, 82), (height - 34, 28)]:
        draw.line([(48, y), (width - 48, y)], fill=(226, 244, 232, alpha), width=1)

    image = Image.alpha_composite(image.convert("RGBA"), overlay.filter(ImageFilter.GaussianBlur(0.28)))
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
