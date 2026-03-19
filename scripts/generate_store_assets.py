from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
ASSETS_ROOT = ROOT / "store-assets"
SCREENSHOTS_ROOT = ASSETS_ROOT / "screenshots"
ICON_PATH = ROOT / "icons" / "icon-128.png"

WHITE = "#ffffff"
RED = "#d71920"
RED_SOFT = "#fde9ea"
BLACK = "#111111"
MUTED = "#666666"
LINE = "#f1c7ca"


def font(size: int, bold: bool = False):
    try:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def load_icon(size: int) -> Image.Image:
    icon = Image.open(ICON_PATH).convert("RGBA")
    return icon.resize((size, size), Image.Resampling.LANCZOS)


def wrap_text(draw, text, font_obj, max_width):
    words = text.split()
    lines = []
    current = []

    for word in words:
        test = " ".join(current + [word])
        if draw.textlength(test, font=font_obj) <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]

    if current:
        lines.append(" ".join(current))

    return lines


def create_brand_asset(width: int, height: int, output_path: Path, label=None, subtitle=None):
    image = Image.new("RGBA", (width, height), WHITE)
    draw = ImageDraw.Draw(image)

    rounded(draw, (0, 0, width - 1, height - 1), 0, WHITE)
    draw.rectangle((0, 0, width, height), fill=WHITE)
    draw.line((0, 0, 0, height), fill=RED, width=max(10, width // 110))
    draw.line((0, height - max(10, height // 40), width, height - max(10, height // 40)), fill=RED_SOFT, width=max(10, height // 40))

    icon_size = int(min(height * 0.5, width * 0.22))
    icon_x = int(width * 0.1)
    icon_y = (height - icon_size) // 2
    image.alpha_composite(load_icon(icon_size), dest=(icon_x, icon_y))

    text_x = icon_x + icon_size + int(width * 0.08)
    title_max_width = width - text_x - int(width * 0.07)
    label_font = font(max(16, height // 22), bold=True)
    title_font = font(84 if width >= 1000 else 52 if width >= 600 else 34, bold=True)
    subtitle_font = font(24 if width >= 1000 else 16 if width >= 600 else 12)

    current_y = int(height * 0.24)

    if label:
        draw.text((text_x, current_y), label.upper(), font=label_font, fill=RED)
        current_y += label_font.size + int(height * 0.05)

    title_lines = ["Open YouTube", "in New Tab"]
    for line in title_lines:
        draw.text((text_x, current_y), line, font=title_font, fill=BLACK)
        current_y += title_font.size + int(height * 0.015)

    if subtitle:
        current_y += int(height * 0.03)
        for line in wrap_text(draw, subtitle, subtitle_font, title_max_width):
            draw.text((text_x, current_y), line, font=subtitle_font, fill=MUTED)
            current_y += subtitle_font.size + int(height * 0.014)

    accent_y = int(height * 0.8)
    accent_w = min(int(width * 0.24), title_max_width)
    rounded(draw, (text_x, accent_y, text_x + accent_w, accent_y + max(10, height // 28)), max(5, height // 40), RED_SOFT)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def main():
    ASSETS_ROOT.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_ROOT.mkdir(parents=True, exist_ok=True)

    create_brand_asset(
        440,
        280,
        ASSETS_ROOT / "promo-small-440x280.png",
        label="Chrome Extension",
        subtitle="Simple red and white branding for the store listing.",
    )
    create_brand_asset(
        1400,
        560,
        ASSETS_ROOT / "promo-marquee-1400x560.png",
        label="Chrome Web Store",
        subtitle="Open standard YouTube watch links in a new adjacent tab.",
    )
    create_brand_asset(
        1280,
        800,
        SCREENSHOTS_ROOT / "screenshot-01-search-results.png",
        label="Search Results",
        subtitle="Open videos beside the current tab without losing your place.",
    )
    create_brand_asset(
        1280,
        800,
        SCREENSHOTS_ROOT / "screenshot-02-home-feed.png",
        label="Home Feed",
        subtitle="Keep your browsing page in place while opening the next video.",
    )
    create_brand_asset(
        1280,
        800,
        SCREENSHOTS_ROOT / "screenshot-03-popup-enabled.png",
        label="Popup Enabled",
        subtitle="A simple on or off toggle controls the behavior instantly.",
    )
    create_brand_asset(
        1280,
        800,
        SCREENSHOTS_ROOT / "screenshot-04-channel-grid.png",
        label="Channel Videos",
        subtitle="Open channel-page videos in a new adjacent tab.",
    )
    create_brand_asset(
        1280,
        800,
        SCREENSHOTS_ROOT / "screenshot-05-popup-disabled.png",
        label="Popup Disabled",
        subtitle="Turn it off any time to restore normal YouTube navigation.",
    )


if __name__ == "__main__":
    main()
