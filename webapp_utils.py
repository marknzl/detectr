import easyocr

from PIL import Image
from re import sub

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


def get_license_plate(filename):
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = \
        read_rgb_image_to_separate_pixel_arrays(f'static/{filename}')

    greyscale_image = compute_rgb_to_greyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    contrast_stretched_image = contrast_stretch(greyscale_image, image_width, image_height)
    std_dev_image = contrast_stretch(
        compute_standard_deviation_image_5x5(contrast_stretched_image, image_width, image_height),
        image_width, image_height)
    thresholded_image = compute_threshold(std_dev_image, 140, image_width, image_height)
    binary_closed_image = binary_close(thresholded_image, image_width, image_height, 3, 3)

    connected_components, labels, initial_pixel_locs = compute_connected_component_labeling(binary_closed_image,
                                                                                            image_width, image_height)

    min_x, max_x, min_y, max_y = get_bounding_box(connected_components, initial_pixel_locs, labels)

    im = Image.open(f'static/{filename}')
    im2 = im.crop((min_x, min_y, max_x, max_y))

    extracted_filename = f'{filename.split(".")[0]}_plate.{filename.split(".")[1]}'
    im2.save(f'static/{extracted_filename}')
    return extracted_filename


def read_license_plate_text(filename):
    reader = easyocr.Reader(['en'])
    res = reader.readtext(f'static/{filename}')
    return res[0][1], round(res[0][2] * 100, 2)


def filter_text(text):
    return sub('[^0-9A-Za-z ,]', '', text)