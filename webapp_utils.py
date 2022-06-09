import easyocr

from PIL import Image
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
    im2 = im.crop((min_x, min_y, max_x, max_y))

    license_plate_filename = f'{filename.split(".")[0]}_plate.{filename.split(".")[1]}'
    im2.save(STATIC_PATH / license_plate_filename)
    return license_plate_filename


def read_license_plate_text(filename):
    reader = easyocr.Reader(['en'])
    res = reader.readtext(str(STATIC_PATH / filename))
    if not res:
        return '<NO TEXT DETECTED>', -100
    plate_text = res[0][1]
    accuracy = round(res[0][2] * 100, 2)
    return plate_text, accuracy


def filter_text(text):
    return sub('[^0-9A-Za-z ,]', '', text)