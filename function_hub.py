'''
Author: songjintao
Description:

'''
import base64
import io
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from utils.watermarker import im_add_mark


def resize_image(img, size):
    # 获取输入图片的宽度和高度
    original_width, original_height = img.size

    # 计算新的宽度和高度，保持原始尺寸比
    aspect_ratio = float(original_width) / float(original_height)
    new_width, new_height = size
    if original_width / original_height > new_width / new_height:
        new_height = int(new_width / aspect_ratio)
    else:
        new_width = int(new_height * aspect_ratio)

    if new_height % 2 == 1:
        new_height -= 1

    if new_width % 2 == 1:
        new_width -= 1

    # 将图片缩放到新尺寸
    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    # 创建一个新的空白图片
    new_img = Image.new('RGB', size, color=(0, 0, 0))

    # 将缩放后的图片粘贴到空白图片上
    paste_x = (size[0] - new_width) // 2
    paste_y = (size[1] - new_height) // 2
    new_img.paste(img, (paste_x, paste_y))

    return new_img, img


def img2b64(img):
    """
    Convert a PIL image to a base64-encoded string.
    """
    buffered = io.BytesIO()
    img.save(buffered, format='PNG')
    data = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return data


def b642img(b64_image: str):
    """
    Convert a base64-encoded string to a PIL image.
    """
    b64_image_data = BytesIO(base64.b64decode(b64_image))
    img = Image.open(b64_image_data)
    return img


# 从PIL Image对象创建NumPy数组
def pil_to_np(image):
    image = np.array(image)
    # print(image.shape)
    if len(image.shape) == 3:
        if image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


# 从NumPy数组创建PIL Image对象
def np_to_pil(array):
    # print(array.shape)
    if len(array.shape) == 3:
        if array.shape[2] == 3:
            array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    return Image.fromarray(array)


def scale_bbox(bbox, rate):
    """
    :param bbox: a tuple of (left, top, right, bottom) representing the bounding box
    :param rate: a float representing the scale rate (> 0)
    :return: scaled bounding box
    """
    left, top, right, bottom = bbox
    width = right - left
    height = bottom - top
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2
    scaled_width = int(width * rate)
    scaled_height = int(height * rate)
    scaled_left = center_x - scaled_width // 2
    scaled_top = center_y - scaled_height // 2
    scaled_right = scaled_left + scaled_width
    scaled_bottom = scaled_top + scaled_height
    return scaled_left, scaled_top, scaled_right, scaled_bottom


def scale_bbox_with_image(image, bbox, rate):
    """
    :param image: PIL.Image object
    :param bbox: a tuple of (left, top, right, bottom) representing the bounding box
    :param rate: a float representing the scale rate (> 0)
    :return: scaled bounding box
    """
    width, height = image.size
    scaled_left, scaled_top, scaled_right, scaled_bottom = scale_bbox(
        bbox, rate)
    if scaled_left < 0:
        scaled_right -= scaled_left
        scaled_left = 0
    if scaled_top < 0:
        scaled_bottom -= scaled_top
        scaled_top = 0
    if scaled_right > width:
        scaled_left -= (scaled_right - width)
        scaled_right = width
    if scaled_bottom > height:
        scaled_top -= (scaled_bottom - height)
        scaled_bottom = height
    return int(scaled_left), int(scaled_top), int(scaled_right), int(scaled_bottom)


def add_watermark(img, watermark_text):
    text_img = im_add_mark(img, watermark_text, size=100)
    return text_img


if __name__ == "__main__":
    dspth = './input_images'
    for image_path in os.listdir(dspth):
        origin_img = cv2.imread(os.path.join(dspth, image_path))
        origin_img = np_to_pil(origin_img)
        origin_img = add_watermark(origin_img, "clothing ai")
        origin_img.show()
        origin_img = pil_to_np(origin_img)
