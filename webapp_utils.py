import easyocr
import os

from PIL import Image, ImageDraw, ImageFont
from re import sub
from pathlib import Path

from image_utils import (
    read_rgb_image_to_separate_pixel_arrays,
    compute_rgb_to_greyscale,
    contrast_stretch,
    compute_standard_deviation_image_5x5,
    compute_threshold,
    binary_close,
    compute_connected_component_labeling,
    get_bounding_box
)

STATIC_PATH = Path('static')


def get_license_plate(filename):
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = \
        read_rgb_image_to_separate_pixel_arrays(STATIC_PATH / filename)

    greyscale_image = compute_rgb_to_greyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    contrast_stretched_image = contrast_stretch(greyscale_image, image_width, image_height)
    std_dev_image = contrast_stretch(
        compute_standard_deviation_image_5x5(contrast_stretched_image, image_width, image_height),
        image_width, image_height)
    thresholded_image = compute_threshold(std_dev_image, 150, image_width, image_height)
    binary_closed_image = binary_close(thresholded_image, image_width, image_height, 4, 4)

    connected_components, labels, initial_pixel_locs = compute_connected_component_labeling(binary_closed_image,
                                                                                            image_width, image_height)

    min_x, max_x, min_y, max_y = get_bounding_box(connected_components, initial_pixel_locs, labels)

    im = Image.open(STATIC_PATH / filename)
    im2 = im.copy()
    draw = ImageDraw.Draw(im)
    font = None
    x_offset = None

    try:
        font = ImageFont.truetype("consola.ttf", 15, encoding="unic")
        x_offset = font.getsize(f'({min_x, min_y})')[0]
    except:
        pass

    
    draw.rectangle(((min_x, min_y), (max_x, max_y)), outline='green', width=5)

    if font:
        draw.text((min_x - x_offset, min_y - 15), f'{(min_x, min_y)}', fill='#FF2D00', font=font)
    else:
        draw.text((min_x, min_y - 15), f'{(min_x, min_y)}', fill='#FF2D00')
    draw.text((max_x, max_y + 7), f'{(max_x, max_y)}', fill='#FF2D00', font=font)
    im.save(STATIC_PATH / filename)

    # Crop license plate using bounding box bounds
    im2 = im2.crop((min_x, min_y, max_x, max_y))

    license_plate_filename = f'{filename.split(".")[0]}_plate.{filename.split(".")[1]}'

    # Save cropped license plate
    im2.save(STATIC_PATH / license_plate_filename)
    return license_plate_filename


def read_license_plate_text(filename):
    if 'hosted' in os.environ:
        reader = easyocr.Reader(['en'], model_storage_directory='models', download_enabled=False)
    else:
        reader = easyocr.Reader(['en'])
    res = reader.readtext(str(STATIC_PATH / filename))
    if not res:
        return '<NO TEXT DETECTED>', -100
    plate_text = res[-1][1]
    accuracy = round(res[-1][2] * 100, 2)
    return plate_text, accuracy


def filter_text(text):
    return sub('[^0-9A-Za-z ,]', '', text)