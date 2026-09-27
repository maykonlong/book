"""Gera ícones simples do leitor a partir das cores e do monograma do site."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def icon(size: int) -> Image.Image:
    image = Image.new("RGB", (1024, 1024), "#13283b")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((205, 205, 819, 819), radius=112, fill="#ad3f2d")
    draw.polygon(
        [
            (307, 710), (307, 314), (382, 314), (512, 498),
            (642, 314), (717, 314), (717, 710), (627, 710),
            (627, 474), (512, 634), (397, 474), (397, 710),
        ],
        fill="#fff7e9",
    )
    return image.resize((size, size), Image.Resampling.LANCZOS)


def main() -> None:
    for size in (180, 192, 512):
        icon(size).save(ASSETS / f"app-icon-{size}.png", optimize=True)


if __name__ == "__main__":
    main()
