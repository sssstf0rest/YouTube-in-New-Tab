from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
ASSETS_ROOT = ROOT / "store-assets"
SCREENSHOTS_ROOT = ASSETS_ROOT / "screenshots"
ICON_PATH = ROOT / "icons" / "icon-128.png"

RED = "#d71920"
RED_DARK = "#a90f15"
RED_SOFT = "#ffe8ea"
WHITE = "#ffffff"
INK = "#231315"
MUTED = "#775154"
LINE = "#f1c7ca"
SHELL = "#f8f8fa"
CHROME = "#f3f4f7"
CARD = "#fff7f7"


def font(size: int, bold: bool = False):
    try:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def add_base_background(image: Image.Image):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    draw.rectangle((0, 0, width, height), fill=WHITE)
    draw.rectangle((0, 0, width, int(height * 0.22)), fill=RED_SOFT)
    draw.polygon(
        [
            (width * 0.58, 0),
            (width, 0),
            (width, height * 0.42),
        ],
        fill="#fff3f4",
    )
    return draw


def load_icon(size: int) -> Image.Image:
    icon = Image.open(ICON_PATH).convert("RGBA")
    return icon.resize((size, size), Image.Resampling.LANCZOS)


def draw_logo_badge(image: Image.Image, xy, size):
    x, y = xy
    badge = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    bdraw = ImageDraw.Draw(badge)
    rounded(bdraw, (0, 0, size - 1, size - 1), 28, WHITE)
    badge.alpha_composite(load_icon(int(size * 0.78)), dest=(int(size * 0.11), int(size * 0.11)))
    image.alpha_composite(badge, dest=(x, y))


def draw_text_block(draw, xy, title, subtitle=None, title_size=48, subtitle_size=22, fill=INK, max_width=None):
    x, y = xy
    title_font = font(title_size, bold=True)
    subtitle_font = font(subtitle_size, bold=False)
    draw.text((x, y), title, font=title_font, fill=fill)

    if subtitle:
        bbox = draw.textbbox((x, y), title, font=title_font)
        next_y = bbox[3] + 12
        if max_width:
            lines = wrap_text(draw, subtitle, subtitle_font, max_width)
            for line in lines:
                draw.text((x, next_y), line, font=subtitle_font, fill=MUTED)
                next_y += subtitle_font.size + 10
        else:
            draw.text((x, next_y), subtitle, font=subtitle_font, fill=MUTED)


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


def draw_browser(draw, box, tabs, active_index, url):
    x, y, w, h = box
    rounded(draw, (x, y, x + w, y + h), 24, WHITE, outline=LINE, width=2)
    rounded(draw, (x, y, x + w, y + 84), 24, CHROME)
    draw.rectangle((x, y + 60, x + w, y + 84), fill=CHROME)

    tab_x = x + 24
    for index, label in enumerate(tabs):
        tab_w = 210 if index == active_index else 185
        tab_h = 40
        fill = WHITE if index == active_index else "#eceef3"
        outline = LINE if index == active_index else "#dde1e8"
        rounded(draw, (tab_x, y + 18, tab_x + tab_w, y + 18 + tab_h), 16, fill, outline=outline, width=1)
        draw.text((tab_x + 18, y + 29), label, font=font(17, bold=index == active_index), fill=INK)
        tab_x += tab_w + 10

    rounded(draw, (x + 24, y + 94, x + w - 24, y + 142), 18, WHITE, outline="#dfe3ea", width=1)
    draw.text((x + 50, y + 108), url, font=font(18), fill=MUTED)
    draw.ellipse((x + 36, y + 110, x + 42, y + 116), fill=RED)
    content_box = (x + 24, y + 160, x + w - 24, y + h - 24)
    rounded(draw, content_box, 18, SHELL)
    return content_box


def draw_search_scene(draw, box, highlight_index=0):
    x1, y1, x2, y2 = box
    rounded(draw, (x1 + 28, y1 + 28, x2 - 28, y1 + 92), 20, WHITE, outline=LINE, width=1)
    draw.text((x1 + 54, y1 + 48), "Search results for: openai", font=font(22, bold=True), fill=INK)

    card_y = y1 + 120
    for idx in range(4):
        outline = RED if idx == highlight_index else LINE
        fill = WHITE if idx == highlight_index else CARD
        rounded(draw, (x1 + 28, card_y, x2 - 28, card_y + 118), 22, fill, outline=outline, width=3 if idx == highlight_index else 1)
        rounded(draw, (x1 + 44, card_y + 18, x1 + 232, card_y + 100), 14, RED_SOFT)
        draw.rectangle((x1 + 72, card_y + 40, x1 + 196, card_y + 78), fill=RED)
        draw.text((x1 + 258, card_y + 26), f"Demo video result {idx + 1}", font=font(24, bold=True), fill=INK)
        draw.text((x1 + 258, card_y + 62), "Open beside the current tab", font=font(18), fill=MUTED)
        card_y += 136


def draw_home_scene(draw, box):
    x1, y1, x2, y2 = box
    draw.text((x1 + 28, y1 + 24), "Home", font=font(22, bold=True), fill=INK)
    start_x = x1 + 28
    start_y = y1 + 72
    gap = 24
    card_w = 244
    card_h = 190

    for row in range(2):
        for col in range(4):
            px = start_x + col * (card_w + gap)
            py = start_y + row * (card_h + gap + 40)
            rounded(draw, (px, py, px + card_w, py + card_h), 22, WHITE, outline=LINE, width=1)
            rounded(draw, (px + 14, py + 14, px + card_w - 14, py + 116), 18, RED_SOFT)
            draw.rectangle((px + 40, py + 42, px + card_w - 40, py + 82), fill=RED)
            draw.text((px + 14, py + 132), "Keep your feed in place", font=font(18, bold=True), fill=INK)
            draw.text((px + 14, py + 156), "Open videos in the next tab", font=font(14), fill=MUTED)


def draw_watch_scene(draw, box):
    x1, y1, x2, y2 = box
    video_box = (x1 + 28, y1 + 28, x1 + 716, y1 + 420)
    rounded(draw, video_box, 22, WHITE, outline=LINE, width=1)
    rounded(draw, (video_box[0] + 18, video_box[1] + 18, video_box[2] - 18, video_box[3] - 18), 18, RED_SOFT)
    draw.polygon(
        [
            (video_box[0] + 300, video_box[1] + 145),
            (video_box[0] + 300, video_box[1] + 255),
            (video_box[0] + 395, video_box[1] + 200),
        ],
        fill=RED,
    )
    draw.text((video_box[0], video_box[3] + 18), "Current video tab", font=font(24, bold=True), fill=INK)
    draw.text((video_box[0], video_box[3] + 54), "Recommendations open beside this tab too.", font=font(18), fill=MUTED)

    sidebar_x = x1 + 756
    item_y = y1 + 28
    for _ in range(4):
        rounded(draw, (sidebar_x, item_y, x2 - 28, item_y + 110), 20, WHITE, outline=LINE, width=1)
        rounded(draw, (sidebar_x + 14, item_y + 14, sidebar_x + 164, item_y + 96), 14, RED_SOFT)
        draw.rectangle((sidebar_x + 38, item_y + 38, sidebar_x + 140, item_y + 72), fill=RED)
        draw.text((sidebar_x + 186, item_y + 24), "Recommended video", font=font(19, bold=True), fill=INK)
        draw.text((sidebar_x + 186, item_y + 56), "Opens in the next tab", font=font(15), fill=MUTED)
        item_y += 126


def draw_popup(image, anchor_xy, enabled=True):
    x, y = anchor_xy
    width = 300
    height = 236
    popup = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    pdraw = ImageDraw.Draw(popup)
    rounded(pdraw, (0, 0, width - 1, height - 1), 20, WHITE, outline=LINE, width=2)
    pdraw.rectangle((0, 0, width, 8), fill=RED)
    pdraw.text((24, 28), "YouTube in New Tab", font=font(24, bold=True), fill=INK)
    pdraw.text((24, 64), "Open video links in a new tab.", font=font(16), fill=MUTED)
    rounded(pdraw, (24, 106, width - 24, 174), 18, RED_SOFT, outline=LINE, width=1)
    pdraw.text((42, 126), "Enabled", font=font(18, bold=True), fill=INK)
    pdraw.text((42, 150), "For /watch links on www.youtube.com", font=font(12), fill=MUTED)
    track_fill = RED if enabled else "#d7d9de"
    pill_text = "On" if enabled else "Off"
    rounded(pdraw, (216, 124, 264, 154), 15, track_fill)
    pdraw.ellipse((234 if enabled else 216, 120, 258 if enabled else 240, 144), fill=WHITE)
    pdraw.text((24, 194), "Status", font=font(14, bold=True), fill=MUTED)
    rounded(pdraw, (86, 188, 146, 214), 13, "#ffecee" if enabled else "#f1f2f4")
    pdraw.text((101, 193), pill_text, font=font(14, bold=True), fill=RED_DARK if enabled else INK)

    shadow = Image.new("RGBA", (width + 30, height + 30), (255, 255, 255, 0))
    sdraw = ImageDraw.Draw(shadow)
    rounded(sdraw, (15, 15, width + 10, height + 10), 24, (215, 25, 32, 32))
    image.alpha_composite(shadow, dest=(x - 15, y - 15))
    image.alpha_composite(popup, dest=(x, y))


def draw_callout(draw, box, text):
    rounded(draw, box, 18, RED)
    x1, y1, x2, y2 = box
    lines = wrap_text(draw, text, font(18, bold=True), x2 - x1 - 34)
    current_y = y1 + 16
    for line in lines:
        draw.text((x1 + 16, current_y), line, font=font(18, bold=True), fill=WHITE)
        current_y += 24


def save(image: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def create_small_promo():
    image = Image.new("RGBA", (440, 280), RED)
    draw = add_base_background(image)
    draw.rectangle((0, 0, 440, 280), fill=RED)
    rounded(draw, (178, 42, 394, 210), 30, WHITE)
    rounded(draw, (44, 74, 228, 206), 26, "#f04b52")
    rounded(draw, (70, 96, 254, 228), 26, "#ff6d73")
    draw_logo_badge(image, (226, 74), 118)
    rounded(draw, (294, 140, 392, 192), 18, RED_SOFT)
    save(image, ASSETS_ROOT / "promo-small-440x280.png")


def create_marquee():
    image = Image.new("RGBA", (1400, 560), WHITE)
    draw = add_base_background(image)
    draw.polygon([(900, 0), (1400, 0), (1400, 560)], fill=RED_SOFT)
    rounded(draw, (864, 70, 1220, 420), 48, RED)
    rounded(draw, (920, 126, 1276, 476), 48, WHITE)
    draw_logo_badge(image, (1004, 172), 188)
    rounded(draw, (772, 178, 970, 438), 40, "#ef4a50")
    rounded(draw, (686, 226, 884, 486), 40, "#ff6b71")
    rounded(draw, (1102, 226, 1300, 486), 40, "#ffc7ca")
    save(image, ASSETS_ROOT / "promo-marquee-1400x560.png")


def create_screenshot_01():
    image = Image.new("RGBA", (1280, 800), WHITE)
    draw = add_base_background(image)
    draw_text_block(
        draw,
        (64, 56),
        "Open videos beside the current tab",
        "Click from search results without losing your place.",
        title_size=42,
        subtitle_size=22,
        max_width=540,
    )
    content = draw_browser(
        draw,
        (64, 170, 1152, 560),
        ["Search results", "Next video"],
        0,
        "https://www.youtube.com/results?search_query=openai",
    )
    draw_search_scene(draw, content, highlight_index=0)
    draw_callout(draw, (898, 196, 1160, 276), "The new video tab opens here.")
    save(image, SCREENSHOTS_ROOT / "screenshot-01-search-results.png")


def create_screenshot_02():
    image = Image.new("RGBA", (1280, 800), WHITE)
    draw = add_base_background(image)
    draw_text_block(
        draw,
        (64, 56),
        "Keep the feed in place",
        "Browse YouTube home or subscriptions and open the next watch page beside it.",
        title_size=42,
        subtitle_size=22,
        max_width=620,
    )
    content = draw_browser(
        draw,
        (64, 170, 1152, 560),
        ["Home", "Current video"],
        1,
        "https://www.youtube.com/watch?v=example",
    )
    draw_home_scene(draw, content)
    draw_callout(draw, (888, 196, 1160, 276), "Your original tab stays exactly where it was.")
    save(image, SCREENSHOTS_ROOT / "screenshot-02-home-feed.png")


def create_screenshot_03():
    image = Image.new("RGBA", (1280, 800), WHITE)
    draw = add_base_background(image)
    draw_text_block(
        draw,
        (64, 56),
        "One simple toggle",
        "Turn the behavior on or off from the toolbar popup.",
        title_size=42,
        subtitle_size=22,
        max_width=580,
    )
    content = draw_browser(
        draw,
        (64, 170, 1152, 560),
        ["Search results"],
        0,
        "https://www.youtube.com/results?search_query=openai",
    )
    draw_search_scene(draw, content, highlight_index=1)
    draw_popup(image, (846, 236), enabled=True)
    save(image, SCREENSHOTS_ROOT / "screenshot-03-popup-enabled.png")


def create_screenshot_04():
    image = Image.new("RGBA", (1280, 800), WHITE)
    draw = add_base_background(image)
    draw_text_block(
        draw,
        (64, 56),
        "Recommendations work too",
        "Open suggested videos beside the current watch page instead of replacing it.",
        title_size=42,
        subtitle_size=22,
        max_width=680,
    )
    content = draw_browser(
        draw,
        (64, 170, 1152, 560),
        ["Current video", "Recommended video"],
        0,
        "https://www.youtube.com/watch?v=current",
    )
    draw_watch_scene(draw, content)
    draw_callout(draw, (860, 196, 1160, 276), "Sidebar recommendations also open in the next tab.")
    save(image, SCREENSHOTS_ROOT / "screenshot-04-watch-page.png")


def create_screenshot_05():
    image = Image.new("RGBA", (1280, 800), WHITE)
    draw = add_base_background(image)
    draw_text_block(
        draw,
        (64, 56),
        "Disable it any time",
        "Use the same popup switch to return to normal YouTube navigation.",
        title_size=42,
        subtitle_size=22,
        max_width=640,
    )
    content = draw_browser(
        draw,
        (64, 170, 1152, 560),
        ["Home"],
        0,
        "https://www.youtube.com/",
    )
    draw_home_scene(draw, content)
    draw_popup(image, (846, 236), enabled=False)
    save(image, SCREENSHOTS_ROOT / "screenshot-05-popup-disabled.png")


def main():
    ASSETS_ROOT.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_ROOT.mkdir(parents=True, exist_ok=True)
    create_small_promo()
    create_marquee()
    create_screenshot_01()
    create_screenshot_02()
    create_screenshot_03()
    create_screenshot_04()
    create_screenshot_05()


if __name__ == "__main__":
    main()
