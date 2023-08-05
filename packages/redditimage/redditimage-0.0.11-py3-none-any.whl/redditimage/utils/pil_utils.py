# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Tuple

# Pip
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def image(width: int, height: int, color: (int, int, int, int) = (0, 0, 0, 0)) -> Image:
    return Image.new("RGBA", (width, height), color)

def text_image(
    text: str,
    font: ImageFont,
    width: Optional[int] = None,
    height: Optional[int] = None,
    fg_color: (int, int, int) = (255, 255, 255),
    bg_color: (int, int, int, int) = (0, 0, 0, 0),
    halo_color: Optional[Tuple[int, int, int, int]] = None,
    wrap_instead_of_font_downscale: bool = True,
    align: str = 'left' # 'center', 'right'
) -> Image:
    org_text = text
    stroke_width = 10 if halo_color is not None else 0
    tw, th = font.getsize_multiline(text, stroke_width=stroke_width)

    width = width or tw

    if tw > width:
        if wrap_instead_of_font_downscale:
            text = wrapped_text(org_text, font, width, height)
            tw, th = font.getsize_multiline(text, stroke_width=stroke_width)
        else:
            font = ImageFont.truetype(font.path, int(float(font.size) * (float(width)/float(tw))))
            tw, th = font.getsize_multiline(text, stroke_width=stroke_width)
    # elif tw < width:
    #     width = tw

    height = height or th

    if th > height:
        font = ImageFont.truetype(font.path, int(float(font.size) * (float(height)/float(th))))
        text = wrapped_text(org_text, font, width, height)
        tw, th = font.getsize_multiline(text, stroke_width=stroke_width)
    # elif th < height:
    #     height = th

    img = image(tw, int(th + int(float(font.size)*0.25)), bg_color)

    ImageDraw.Draw(img).text(
        (0, 0),
        text,
        fill=fg_color,
        font=font,
        align=align,
        stroke_fill=halo_color,
        stroke_width=stroke_width
    )

    return img

def wrapped_text(text: str, font: ImageFont, max_width: int, max_height: Optional[int] = None) -> str:
    max_height = max_height or 100000000
    one_line_width = font.getsize(text)[0]

    if one_line_width < max_width:
        return text

    avg_char_width = float(one_line_width) / float(len(text))
    limit = float(max_width) / avg_char_width * 0.96

    _lines = text.split('\n')
    lines = []

    import textwrap
    wrapper = textwrap.TextWrapper(width=limit)

    for line in _lines:
        lines.append('\n'.join(wrapper.wrap(text=line)))
    
    return '\n'.join(lines).strip()

def resized(img: Image, width: Optional[int] = None, height: Optional[int] = None) -> Image:
    w, h = img.size
    width = width or w
    height = height or h

    ratio = 1

    if w != width:
        ratio = float(width)/float(w)

    if height != h:
        _ratio = float(height)/float(h)

        if _ratio < ratio:
            ratio = _ratio

    if ratio == 1:
        return img

    return img.resize((int(float(w)*ratio), int(float(h)*ratio)), Image.ANTIALIAS)


def __draw_text_with_halo(img, position, text, font, col, halo_col):
    halo = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).text(position, text, font = font, fill = halo_col)
    blurred_halo = halo.filter(ImageFilter.BLUR)
    ImageDraw.Draw(blurred_halo).text(position, text, font = font, fill = col)

    return Image.composite(img, blurred_halo, ImageChops.invert(blurred_halo))

# ---------------------------------------------------------------------------------------------------------------------------------------- #