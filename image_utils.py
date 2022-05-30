from png import Reader

def read_rgb_image_to_separate_pixel_arrays(input_filename) -> tuple:
    image_reader = Reader(filename=input_filename)
    (image_width, image_height, rgb_image_rows, _) = image_reader.read()

    print(f'Read image with width={image_width}, height={image_height}')

    pixel_array_r: list[int] = []
    pixel_array_g: list[int] = []
    pixel_array_b: list[int] = []

    for row in rgb_image_rows:
        pixel_row_r: list[int] = []
        pixel_row_g: list[int] = []
        pixel_row_b: list[int] = []
        r: int = 0
        g: int = 0
        b: int = 0
        for elem in range(0, len(row)):
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

def create_initialized_greyscale_pixel_array(image_width, image_height, init_value=0) -> list[list[int]]:
    return [[init_value for _ in range(image_width)] for _ in range(image_height)]

def compute_rgb_to_greyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height) -> list[list[int]]:
    greyscale_pixel_array = create_initialized_greyscale_pixel_array(image_width, image_height)
    for row in range(0, image_height):
        for col in range(0, image_width):
            g = 0.299 * pixel_array_r[row][col] + (0.587 * pixel_array_g[row][col]) + (0.114 * pixel_array_b[row][col])
            greyscale_pixel_array[row][col] = int(round(g))
    return greyscale_pixel_array