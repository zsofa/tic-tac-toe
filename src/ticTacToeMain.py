import cv2
import numpy as np
from dateutil.tz import resolve_imaginary
import matplotlib.pyplot as plt

img_path = "assets/test2.png"
color_img = cv2.imread(img_path)
gray_image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

#img_blank = np.zeros((450, 450, 3), np.uint)

if color_img is None or gray_image is None:
    FileNotFoundError("Could not open or find the image.")


cv2.imshow("Grayscale Image", gray_image)
cv2.waitKey(0)

# Gaussian blur and edge detection
# blurred = cv2.GaussianBlur(gray_image, (5,5), 0)
# Use Adaptive Thresholding
adaptive_thresh = cv2.adaptiveThreshold(
    gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

cv2.imshow("Adaptive Threshold", adaptive_thresh)
cv2.waitKey(0)

# edge detection
edges = cv2.Canny(adaptive_thresh, 30, 150)

cv2.imshow("Edges detected", edges)
cv2.waitKey(0)

# Detect the grid
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if not contours:
    raise ValueError("No contours found in the image. Check the edge detection step or input image.")

print(f"Number of contours found: {len(contours)}")
print(f"Type of first contour (if available): {type(contours[0])}")

# Draw contours on original img
img_with_contours = color_img.copy()
cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2)

cv2.imshow("Contours found", img_with_contours)
cv2.waitKey(0)


# filtering out the grid based on the size
grid_contour = max(contours, key=cv2.contourArea)


