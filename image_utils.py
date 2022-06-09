from png import Reader
from math import sqrt
from collections import deque

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

def compute_dilation_3x3(pixel_array, image_width, image_height) -> list[list[int]]:
    new_image = create_initialized_greyscale_pixel_array(image_width, image_height)
    for y in range(0, image_height):
        for x in range(0, image_width):
            if pixel_array[y][x]:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if out_of_bounds(x + dx, y + dy, image_width, image_height):
                            continue
                        new_image[y + dy][x + dx] = 1
                new_image[y][x] = 1
    return new_image

def compute_erosion_3x3(pixel_array, image_width, image_height) -> list[list[int]]:
    new_image = create_initialized_greyscale_pixel_array(image_width, image_height)

    for y in range(0, image_height):
        for x in range(0, image_width):
            if not pixel_array[y][x]:
                continue
            valid = True
            for dy in [-1, 0, 1]:
                if not valid:
                    break

                for dx in [-1, 0, 1]:
                    if out_of_bounds(x + dx, y + dy, image_width, image_height):
                        valid = False
                        break

                    if not pixel_array[y + dy][x + dx]:
                        valid = False
                        break
            if valid:
                new_image[y][x] = 1

    return new_image

def binary_close(pixel_array, image_width, image_height, dilation_iterations=1, erosion_iterations=1):
    dilated_image = None
    for _ in range(0, dilation_iterations):
        if dilated_image:
            dilated_image = compute_dilation_3x3(dilated_image, image_width, image_height)
        else:
            dilated_image = compute_dilation_3x3(pixel_array, image_width, image_height)
    eroded_image = None
    for _ in range(0, erosion_iterations):
        if eroded_image:
            eroded_image = compute_erosion_3x3(eroded_image, image_width, image_height)
        else:
            eroded_image = compute_erosion_3x3(dilated_image, image_width, image_height)
    return eroded_image

def compute_connected_component_labeling(pixel_array, image_width, image_height):
    new_image = [[0 for _ in range(0, image_width)] for _ in range(0, image_height)]
    curr_label = 1
    mappings = dict()
    initial_pixel_locs = dict()
    visited = set()

    offsets = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for y in range(0, image_height):
        for x in range(0, image_width):
            if pixel_array[y][x] and (x, y) not in visited:
                queue = deque()
                queue.append((x, y))
                initial_pixel_locs[curr_label] = (x, y)
                visited.add((x, y))
                mappings[curr_label] = 0

                while len(queue):
                    x1, y1 = queue.pop()
                    new_image[y1][x1] = curr_label

                    mappings[curr_label] += 1

                    for dx, dy in offsets:
                        x_offset = x1 + dx
                        y_offset = y1 + dy
                        if out_of_bounds(x_offset, y_offset, image_width, image_height):
                            continue

                        if pixel_array[y_offset][x_offset] and (x_offset, y_offset) not in visited:
                            queue.append((x_offset, y_offset))
                            visited.add((x_offset, y_offset))

                curr_label += 1

    return new_image, mappings, initial_pixel_locs

def dfs(pixel_array, x, y, label):
    min_x = float('infinity')
    max_x = -1
    min_y = float('infinity')
    max_y = -1

    stack = [(x, y)]
    visited = set()
    visited.add((x, y))

    while stack:
        x1, y1 = stack[-1]
        min_x = min(x1, min_x)
        max_x = max(x1, max_x)
        min_y = min(y1, min_y)
        max_y = max(y1, max_y)
        found_neighbour = False

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                x_offset = x1 + dx
                y_offset = y1 + dy
                if out_of_bounds(x_offset, y_offset, len(pixel_array[0]), len(pixel_array)):
                    continue
                neighbour = (x_offset, y_offset)
                if pixel_array[y_offset][x_offset] == label and neighbour not in visited:
                    stack.append(neighbour)
                    visited.add(neighbour)
                    found_neighbour = True
                    break

        if not found_neighbour:
            stack.pop()

    width = max_x - min_x
    height = max_y - min_y
    aspect_ratio = width / height
    return min_x, max_x, min_y, max_y, 1.5 <= aspect_ratio <= 5

def get_bounding_box(connected_components, initial_pixel_locs, labels):
    sorted_labels = sorted(labels.items(), key=lambda l: l[1], reverse=True)

    min_x = float('infinity')
    max_x = -1
    min_y = float('infinity')
    max_y = -1

    for label, _ in sorted_labels:
        x, y = initial_pixel_locs[label]
        # Calculate min/max 'x' and min/max 'y' for connected component via DFS
        mi_x, ma_x, mi_y, ma_y, valid = dfs(connected_components, x, y, label)
        if valid:
            min_x, max_x, min_y, max_y = mi_x, ma_x, mi_y, ma_y
            break

    return min_x, max_x, min_y, max_y