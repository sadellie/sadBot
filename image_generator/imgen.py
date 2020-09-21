#    Copyright 2020 Elshan Agaev
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Image generator
#TODO REFACTOR
"""

from os.path import dirname

from PIL import Image
from PIL import ImageFont as Font
from PIL.ImageDraw import Draw
from glitch_this import ImageGlitcher

from image_generator import gradient

# Folder with images
directory = dirname(__file__) + '/imgen_files/'

glitcher = ImageGlitcher()


def glitch(image, seed: int = None):
    """
    Add add_glitch effect

    :param image: Image
    :param seed: Optional. Seed for a specific add_glitch. Cool seeds 5353, 5252
    :return: Glitched image
    """
    glitch_img = glitcher.glitch_image(image, 1.7, color_offset=True, cycle=True, seed=seed)
    return glitch_img


width = 1366
height = 768

main_image = Image.new(mode='RGBA', size=(width, height), color=(140, 50, 90, 0))
image_filter = Image.new(mode='RGBA', size=(width, height), color=(40, 0, 97, 50))
background_image = Image.new(mode='RGBA', size=(width, height), color=(0, 0, 0, 255))
text_texture = Image.new(mode='RGBA', size=(width, height), color=(0, 0, 0, 255))


def add_text(
        draw,
        text: str,
        font_file: str,
        text_size: int,
        color,
        v_off=0,
        h_off=0,
        stroke_color=None,
        shadow=False,
        shadow_color: str = None):
    """
    Add text to image


    :param draw: ImageDraw
    :param text: Text
    :param font_file: Path to font file
    :param text_size: Text size
    :param color: Text color
    :param v_off: Optional. Vertical offset
    :param h_off: Optional. Horizontal offset
    :param stroke_color: Optional. Stroke color
    :param shadow: Optional. Shadow
    :param shadow_color: Optional. Shadow color
    """
    f = Font.truetype(font=directory + "Fonts/" + font_file, size=text_size)
    w, h = draw.textsize(text=text, font=f)
    x = (width - w) / 2 + h_off
    y = (height - h) / 2 + v_off

    # Stroke
    stroke_width = None
    if stroke_color is not None:
        stroke_width = int(text_size / 24)

    # Shadow
    if shadow:
        draw.text(xy=(x + 5, y + 5),
                  text=text,
                  align="center",
                  font=f,
                  fill=shadow_color,
                  stroke_width=stroke_width)
    # Text
    draw.text(
        xy=(x, y),
        text=text,
        align="center",
        font=f,
        fill=color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color)


def text_image_builder(text1: str, text2: str):
    """
    Add all 2 texts

    :param text1: Main text
    :param text2: Additional text
    """
    d = Draw(main_image)
    dt = Draw(background_image)

    add_text(draw=dt,
             text=text1,
             font_file='commando.ttf',
             text_size=245,
             color=(0, 220, 235, 0),
             stroke_color=(255, 255, 255, 255))

    # Dots
    add_text(draw=dt,
             text=":           :",
             font_file='artbrush.ttf',
             text_size=196,
             color=(0, 220, 235, 0),
             stroke_color=(255, 255, 255, 255),
             v_off=-24)

    # Dots
    add_text(draw=dt,
             text=":",
             font_file='artbrush.ttf',
             text_size=196,
             color=(0, 220, 235, 0),
             stroke_color=(255, 255, 255, 255),
             v_off=-24,
             h_off=-11)

    add_text(draw=d,
             text=text2,
             font_file='artbrush.ttf',
             text_size=186,
             color="red",
             v_off=130)


def create_gradient(image, colors: list, x2=None, y2=None, x1=0, y1=0):
    """
    Add gradient to image

    :param y1: Start y coordinate
    :param x1: Start x coordinate
    :param x2: End y coordinate
    :param y2: End x coordinate
    :param image: Image
    :param colors: Gradient colors
    """
    if x2 is None:
        x2 = image.width
    if y2 is None:
        y2 = image.height
    color_palette = colors
    region = gradient.Rect(x2=x2,
                           y2=y2,
                           x1=x1,
                           y1=y1)
    draw = Draw(image)
    gradient.vert_gradient(draw, region, gradient.gradient_color, color_palette)


def generate_photo(t1: str, t2: str, filename: str, add_glitch: bool = False, seed=None, show_result: bool = False):
    """
    Main function to generate image

    :param show_result: If true will show result
    :param add_glitch: If true will add glitch effect
    :param t1: Main text
    :param t2: Optional text 2
    :param filename: Name of the file
    :param seed: Optional. Glitch seed
    :return: Path to generated image
    """

    center_coord = 24

    create_gradient(text_texture,
                    [(4, 0, 62), (85, 142, 229), (255, 255, 255)],
                    y1=int(height / 2 - 64),
                    y2=int(height / 2 + center_coord))
    create_gradient(text_texture,
                    [(42, 0, 42), (233, 64, 235), (255, 255, 255)],
                    y1=int(height / 2 + center_coord),
                    y2=int(height / 2 + 160))
    create_gradient(background_image,
                    [(62, 0, 119), (43, 0, 43)])

    text_image_builder(t1, t2)
    pica = Image.alpha_composite(background_image, main_image)
    pica = Image.alpha_composite(text_texture, pica)
    pica = Image.alpha_composite(pica, image_filter)

    if add_glitch:
        pica = glitch(pica, seed=seed)
    if show_result:
        pica.show()

    path_to_save = directory + filename + ".png"
    pica.save(path_to_save)
    return path_to_save
