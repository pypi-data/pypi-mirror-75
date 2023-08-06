import cv2 as cv
import numpy as np
import os
from math import floor
import time


def load_images(path):
    for filename in os.listdir(path):
        fullpath = os.path.join(path, filename)
        yield cv.imread(fullpath, cv.IMREAD_UNCHANGED)


def convert_images_colors(images_list):
    for image in images_list:
        yield Converter.convert_colors(image)


def convert_images_sizes(images_list, size):
    for image in images_list:
        yield Converter.resize(image, size=size)


def binary_search(arr, l, r, x):
    global mid
    if r >= l:
        mid = l + (r - l)//2
        if arr[mid] == x:
            return arr[mid]

        elif arr[mid] > x:
            return binary_search(arr, l, mid-1, x)

        else:
            return binary_search(arr, mid+1, r, x)

    else:
        return arr[mid]



class Converter(object):

    @staticmethod
    def load(path):
        return cv.imread(path, cv.IMREAD_UNCHANGED)

    @staticmethod
    def resize(image, size=None, scale_percent=None):
        if scale_percent:
            ratio = scale_percent / 100
            raw_w, raw_h, _ = image.shape
            return cv.resize(image, ( int(raw_w * ratio), int(raw_h * ratio) ))
        elif size:
            return cv.resize(image, size)
        return image

    @staticmethod
    def convert_colors(image, converter=cv.COLOR_BGR2GRAY):
        return cv.cvtColor(image, converter)



class MosaicGenerator(object):
    def __init__(self, image, images, small_images_size,
                 new_image_size=None, ratio=None, filename='default.jpg'):

        self.images = images
        self.small_images_size = small_images_size

        self.image = image
        self.new_image_size = new_image_size

        self.ratio = ratio

        self.filename = filename
        self.mosaic = None

    def __repr__(self):
        return self.mosaic

    @staticmethod
    def _get_average_gray_value(image):
        """ calculate average gray value of given picture area"""
        lines = len(image)
        pixels_in_line = len(image[0])

        s = sum(list(map(sum, image)))
        return int(s // (lines * pixels_in_line))

    @staticmethod
    def _get_image_shape(image):
        try:
            height, width, _ = image.shape
        except ValueError:
            height, width = image.shape
        return height, width

    def _create_small_images_dict(self):
        small_images_dict = {}
        for image in self.images:
            avg_gray = self._get_average_gray_value(image)
            small_images_dict.update({avg_gray: image})
        return small_images_dict

    def _process_image(self):
        sample_small_image = self.images[0]
        small_width, small_height = self._get_image_shape(sample_small_image)

        if self.new_image_size:
            new_width, new_height = self.new_image_size
        else:
            width, height = self._get_image_shape(self.image)
            new_width = (width // 1) * self.ratio
            new_height = (height // 1) * self.ratio

        processed_width = (new_width // small_width) * small_width
        processed_height = (new_height // small_height) * small_height

        self.image = Converter.convert_colors(Converter.resize(self.image, (processed_height, processed_width)))

    def _process_small_images(self):
        self.images = list(convert_images_sizes(self.images, self.small_images_size))
        self.images = list(convert_images_colors(self.images))

    def create(self):
        self._process_small_images()
        self._process_image()
        self.mosaic = self.image

        image_height, image_width = self._get_image_shape(self.image)
        small_width, small_height = self.small_images_size

        small_images_dict = self._create_small_images_dict()
        small_images_values = list(sorted(small_images_dict.keys()))
        for y in range(0, image_height, small_height):
            for x in range(0, image_width, small_width):
                area = self.image[y:y+small_height, x:x+small_width]

                area_value = self._get_average_gray_value(area)
                best_value = binary_search(small_images_values, 0, len(small_images_values) - 1, area_value)
                best_small_picture = small_images_dict[best_value]
                self.mosaic[y:y+small_height, x:x+small_width] = best_small_picture
        return self.mosaic


