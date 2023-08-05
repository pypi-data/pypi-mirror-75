import numpy as np
from PIL import Image
import requests


def load_image(path, resize_height, resize_width, gray, normalization):
    image = Image.open(path)
    input_image = image.resize((resize_width, resize_height))
    if gray:
        input_image = np.array(input_image.convert('L'))
    else:
        input_image = np.array(input_image.convert('RGB'))
    if normalization:
        input_image = input_image / 255
    return input_image


def download_image(image_download_url):
    image_download_response = requests.get(image_download_url)
    if image_download_response.ok:
        image = np.asarray(bytearray(image_download_response.content), dtype="uint8")
        return image
    return None


def draw_rectangle(draw, points, color, width):
    draw.line([(points[0], points[1]), (points[2], points[1])], fill=color, width=width)
    draw.line([(points[2], points[1]), (points[2], points[3])], fill=color, width=width)
    draw.line([(points[2], points[3]), (points[0], points[3])], fill=color, width=width)
    draw.line([(points[0], points[3]), (points[0], points[1])], fill=color, width=width)
    return draw
