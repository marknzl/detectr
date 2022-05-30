from matplotlib import pyplot
from image_utils import (
    compute_dilation_3x3,
    compute_erosion_3x3,
    compute_threshold,
    read_rgb_image_to_separate_pixel_arrays,
    compute_rgb_to_greyscale,
    contrast_stretch,
    compute_standard_deviation_image_5x5
)


def main():
    input_filename = 'numberplate5.png'
    image_width, image_height, px_array_r, px_array_g, px_array_b = read_rgb_image_to_separate_pixel_arrays(input_filename)

    greyscale_image = compute_rgb_to_greyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    contrast_stretched_image = contrast_stretch(greyscale_image, image_width, image_height)
    std_dev_image = contrast_stretch(compute_standard_deviation_image_5x5(contrast_stretched_image, image_width, image_height), image_width, image_height)
    thresholded_image = compute_threshold(std_dev_image, 147, image_width, image_height)

    dilated_image = compute_dilation_3x3(thresholded_image, image_width, image_height)
    for _ in range(0, 2):
        dilated_image = compute_dilation_3x3(dilated_image, image_width, image_height)
    eroded_image = compute_erosion_3x3(dilated_image, image_width, image_height)
    for _ in range(0, 3):
        eroded_image = compute_erosion_3x3(eroded_image, image_width, image_height)

    fig1, axs1 = pyplot.subplots(2, 2)

    axs1[0, 0].set_title('Standard deviation image')
    axs1[0, 0].imshow(std_dev_image, cmap='gray')

    axs1[0, 1].set_title('Thresholded image')
    axs1[0, 1].imshow(thresholded_image, cmap='gray')

    axs1[1, 0].set_title('Morphographically closed image')
    axs1[1, 0].imshow(eroded_image, cmap='gray')

    pyplot.show()

if __name__ == '__main__':
    main()