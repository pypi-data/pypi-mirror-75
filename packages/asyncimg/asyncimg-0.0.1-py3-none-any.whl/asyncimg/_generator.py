import os
from PIL import Image, ImageFilter, ImageChops, ImageDraw, ImageFont
from io import BytesIO
from colorthief import ColorThief

lovers_bg = os.path.join(os.path.dirname(__file__), 'assets', 'love.png')


def get_bytes(final_image):
    final_bytes = BytesIO()
    final_image.save(final_bytes, 'png')
    final_bytes.seek(0)

    return final_bytes


def generate_lovers(boy_image_bytes, girl_image_bytes, bg_path):
    background = Image.open(bg_path).convert("RGBA")

    boy_image = Image.open(boy_image_bytes).convert("RGBA").resize((325, 325)).rotate(3, expand=True)
    girl_image = Image.open(girl_image_bytes).convert("RGBA").resize((325, 325)).rotate(5, expand=True)

    blank = Image.new("RGBA", background.size, (255, 255, 255, 0))

    blank.paste(boy_image, (240, 330))
    blank.paste(girl_image, (650, 278))

    final_image = Image.alpha_composite(blank, background)

    final_bytes = get_bytes(final_image)

    return final_bytes


def generate_frame(image_bytes, bg_path):
    holder = Image.open(bg_path).convert("RGBA")

    profile = Image.open(image_bytes).convert("RGBA").resize((130, 130))

    blank = Image.new("RGBA", holder.size, (255, 255, 255, 0))
    blank.paste(profile, (265, 155))

    background = profile.resize((442, 442)).filter(ImageFilter.GaussianBlur(radius=3))

    final_image = Image.alpha_composite(blank, holder)
    final_image = Image.alpha_composite(background, final_image)

    final_bytes = get_bytes(final_image)

    return final_bytes


def generate_stars(image_bytes, filter_path):
    profile = Image.open(image_bytes).convert("RGBA")
    filter_ = Image.open(filter_path).convert("RGBA").resize(profile.size)

    final_image = ImageChops.add(profile, filter_, 1, 0)

    final_bytes = get_bytes(final_image)

    return final_bytes


def generate_colors(image_bytes, font_path):
    image_ct = ColorThief(image_bytes)
    image_pil = Image.open(image_bytes).resize((500, 500)).convert("RGBA")

    colors = ColorThief.get_palette(image_ct, color_count=5)

    blank = Image.new("RGBA", (200, 500), (255, 255, 255, 0))
    holder = Image.new("RGBA", (720, 500))
    draw = ImageDraw.Draw(blank)

    start = 0
    font = ImageFont.truetype(font_path, 15)
    for color in colors:
        draw.ellipse((0, start, 100, start + 100), fill=color)
        draw.text(
            (120, start + 40), "#%02x%02x%02x" % color, (255, 255, 255), font=font
        )
        start += 100

    holder.paste(image_pil, (220, 0))
    holder.paste(blank, (0, 0))

    final_bytes = get_bytes(holder)

    return final_bytes
