from matplotlib import pyplot
from matplotlib.patches import Rectangle
from image_utils import (
    binary_close,
    compute_threshold,
    get_bounding_box,
    read_rgb_image_to_separate_pixel_arrays,
    compute_rgb_to_greyscale,
    contrast_stretch,
    compute_standard_deviation_image_5x5,
    binary_close,
    compute_connected_component_labeling,
    get_valid_labels,
)


DILATION_ITERATIONS = 3
EROSION_ITERATIONS = 3
THRESHOLD = 140

def main():
    input_filename = 'numberplate3.png'
    output_filename = input_filename.split('.')[0] + '_output.png'
    image_width, image_height, px_array_r, px_array_g, px_array_b = read_rgb_image_to_separate_pixel_arrays(input_filename)

    greyscale_image = compute_rgb_to_greyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    contrast_stretched_image = contrast_stretch(greyscale_image, image_width, image_height)
    std_dev_image = contrast_stretch(compute_standard_deviation_image_5x5(contrast_stretched_image, image_width, image_height), image_width, image_height)
    thresholded_image = compute_threshold(std_dev_image, THRESHOLD, image_width, image_height)

    binary_closed_image = binary_close(thresholded_image, image_width, image_height, DILATION_ITERATIONS, EROSION_ITERATIONS)

    connected_components, labels, initial_pixel_locs = compute_connected_component_labeling(binary_closed_image,
                                                                                            image_width, image_height)
    min_x, max_x, min_y, max_y = get_bounding_box(connected_components, initial_pixel_locs, labels)

    fig1, axs1 = pyplot.subplots(2, 2)

    axs1[0, 0].set_title('Standard deviation image')
    axs1[0, 0].imshow(std_dev_image, cmap='gray')

    axs1[0, 1].set_title('Thresholded image')
    axs1[0, 1].imshow(thresholded_image, cmap='gray')

    axs1[1, 0].set_title('Binary closed image')
    axs1[1, 0].imshow(binary_closed_image, cmap='gray')

    axs1[1, 1].set_title('Final image of detection')
    axs1[1, 1].imshow(px_array_r, cmap='gray')

    axs1[1, 1].set_title('Final image of detection')
    axs1[1, 1].imshow(px_array_r, cmap='gray')
    rect = Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, linewidth=1,
                     edgecolor='g', facecolor='none')
    axs1[1, 1].add_patch(rect)
    extent = axs1[1, 1].get_window_extent().transformed(fig1.dpi_scale_trans.inverted())
    pyplot.savefig(output_filename, bbox_inches=extent, dpi=600)



    pyplot.show()

if __name__ == '__main__':
    main()