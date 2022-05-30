from png import Reader
from math import sqrt

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

def contrast_stretch(pixel_array, image_width, image_height) -> list[list[int]]:
    ret = create_initialized_greyscale_pixel_array(image_width, image_height)

    f_min = 255
    f_max = 0
    for row in range(0, image_height):
        for col in range(0, image_width):
            pixel_val = pixel_array[row][col]
            f_max = max(f_max, pixel_val)
            f_min = min(f_min, pixel_val)

    g_min = 0
    g_max = 255

    for row in range(0, image_height):
        for col in range(0, image_width):
            pixel_val = pixel_array[row][col]
            if f_max == f_min:
                s_out = g_min
            else:
                s_out = (pixel_val - f_min) * ((g_max - g_min) / (f_max - f_min)) + g_min
            if s_out < g_min:
                ret[row][col] = g_min
            elif (g_min <= s_out <= g_max):
                ret[row][col] = round(s_out)
            else:
                ret[row][col] = g_max

    return ret

def out_of_bounds(x, y, image_width, image_height):
    return (x < 0) or (x >= image_width) or (y < 0) or (y >= image_height)

def compute_standard_deviation_image_5x5(pixel_array, image_width, image_height) -> list[list[int]]:
    new_image = create_initialized_greyscale_pixel_array(image_width, image_height, 0)
    for y in range(0, image_height):
        for x in range(0, image_width):
            curr_total = 0
            temp = []
            for dy in [-2, -1, 0, 1, 2]:
                for dx in [-2, -1, 0, 1, 2]:
                    if out_of_bounds(x + dx, y + dy, image_width, image_height):
                        continue
                    curr_total += pixel_array[y + dy][x + dx]
                    temp.append(pixel_array[y + dy][x + dx])
                    
            mean = curr_total / 25
            deviation_sum = 0
            
            for num in temp:
                deviation_sum += (num - mean) ** 2
            
            variance = deviation_sum / 25
            std_dev = sqrt(variance)
            new_image[y][x] = std_dev
    return new_image

def compute_threshold(pixel_array, threshold_value, image_width, image_height) -> list[list[int]]:
    ret = create_initialized_greyscale_pixel_array(image_width, image_height)
    for row in range(0, image_height):
        for col in range(0, image_width):
            val = 255 if pixel_array[row][col] >= threshold_value else 0
            ret[row][col] = val
    return ret