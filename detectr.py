from matplotlib import pyplot
from image_utils import (
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
    std_dev_image = compute_standard_deviation_image_5x5(contrast_stretched_image, image_width, image_height)

    fig1, axs1 = pyplot.subplots(2, 2)

    axs1[0, 0].set_title('test')
    axs1[0, 0].imshow(std_dev_image, cmap='gray')
    pyplot.show()

if __name__ == '__main__':
    main()