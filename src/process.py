import cv2
import numpy as np

def pre_process(img):
    gray_image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(gray_image, (5,5), 1)
    adaptive_threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return adaptive_threshold
