from scipy.optimize import linear_sum_assignment
import cv2
from scipy.ndimage import binary_erosion, gaussian_filter
import math
import tensorflow
import numpy as np
from PIL import Image, ImageFilter

model = tensorflow.saved_model.load('segment')
classes = ["empty",  "pill", ]


def segment_core(img):
    img = img.resize((256, 256))
    inp_numpy = np.array(img)[None]
    inp = tensorflow.constant(inp_numpy, dtype='float32')

    segmentation_output = model(inp)[0].numpy().argmax(-1)
    return segmentation_output


def segment(img: Image.Image):
    seg_img_array = segment_core(img).astype(np.uint8)
    seg_img_array[seg_img_array != 0] = 255
    seg_img_array = scale_array(seg_img_array, img.size[::-1])
    seg_img = Image.fromarray(seg_img_array, "L")
    seg_img = seg_img.filter(ImageFilter.GaussianBlur(radius=20))
    seg_img_array = np.array(seg_img)

    seg_img_array[seg_img_array != 255] = 0

    seg_img = Image.fromarray(seg_img_array, "L")
    seg_img = seg_img.filter(ImageFilter.GaussianBlur(radius=20))
    seg_img_array = np.array(seg_img)
    seg_img_array[seg_img_array != 0] = 255
    return Image.fromarray(seg_img_array, "L")


def calculate_distance_matrix(points):
    n = len(points)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i, j] = np.linalg.norm(
                    np.array(points[i]) - np.array(points[j]))
            else:
                dist_matrix[i, j] = np.inf  # Large value to avoid self-pairing
    return dist_matrix


def minimum_weight_matching(points):
    dist_matrix = calculate_distance_matrix(points)
    row_ind, col_ind = linear_sum_assignment(dist_matrix)
    matched_pairs = [(points[i], points[j]) for i, j in zip(row_ind, col_ind)]
    return matched_pairs


def find_outline(arr):
    eroded = binary_erosion(arr)
    outline = arr & ~eroded
    return outline


def find_concave_points(image, radius=10):
    outline = find_outline(image)
    coords = np.argwhere(outline)
    concave_map = np.zeros(image.shape, dtype=bool)

    for coord in coords:
        degree = 0
        while image[coord[0]+round(math.sin(degree*math.pi/180)*radius), coord[1]+round(math.cos(degree*math.pi/180)*radius)]:
            degree += 1
        while not image[coord[0]+round(math.sin(degree*math.pi/180)*radius), coord[1]+round(math.cos(degree*math.pi/180)*radius)]:
            degree += 1
        angle = 0
        degree -= 1
        while not image[coord[0]+round(math.sin(degree*math.pi/180)*radius), coord[1]+round(math.cos(degree*math.pi/180)*radius)]:
            degree -= 1
            angle += 1
        if angle < 140:
            concave_map[*coord] = True

    concave_map = np.logical_and(gaussian_filter(
        concave_map.astype(float), 10).astype(bool), outline)
    return concave_map


def draw_line(array, start, end, color,width):
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        array[int(y0-width/2):int(y0+width/2), int(x0-width/2):int(x0+width/2)] = color  # Set the pixel to the color (True or False)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def segment_and_disconnect(img: Image.Image):
    segmented = segment(img)
    seg_np = np.array(segmented).astype(bool)
    concave_map = find_concave_points(seg_np)
    contours = cv2.findContours(concave_map.astype(
        np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    points = []
    for contour in contours:
        contour = [p[::-1] for p, *_ in contour]
        point = [int(sum(y) / len(y)) for y in zip(*contour)]
        points.append(point)
    
    for a, b in minimum_weight_matching(points):
        print(a,b)
        draw_line(seg_np, a[::-1], b[::-1], False, 2)

    return Image.fromarray(seg_np.astype(np.uint8)*255, "L")


def scale_array(arr, new_size):
    """
    Resizes a NumPy array like an image.
    Parameters:
        x (ndarray): The original NumPy array to be resized.
        new_size (tuple): The desired shape of the new array.
    Returns:
        ndarray: The resized NumPy array.
    """
    factors = tuple(old/new for new, old in zip(new_size, arr.shape))

    def pixel(x, y):
        return arr[int(x*factors[0]), int(y*factors[1])]
    g = np.vectorize(pixel)
    return np.fromfunction(g, new_size)
