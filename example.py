import cv2
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, image_rotate
from weiner import weiner_filter, metric, pad_with
import numpy as np

im = imageResize(cv2.imread("dataset/kangaroo/image_0001.jpg", 0))
# cv2.imshow('im', im)
# cv2.waitKey(0)
print im.shape


gaussian_kernel = Gaussian(2, 1)
p = convolution2d(im, gaussian_kernel, 0)
gaussian_blur = np.pad(p, (im.shape[0]-p.shape[0])/2, pad_with, padder=1)
print gaussian_blur.shape
noise = gaussianNoise(im, 1)
noisy_image = gaussian_blur + noise
# cv2.imshow('blurred image', noisy_image)
# cv2.imshow('noise image', noisy_image/255)
# # defocus_blur = defocus(im, , 0)

# # print gaussian_blur
# # cv2.imshow('gaussian_blur', gaussian_blur)
# # cv2.imshow('im', im)
# cv2.waitKey(0)
# # cv2.imshow('gaussian blur', gaussian_blur)

restored_image = image_rotate(np.real(weiner_filter(noisy_image, gaussian_kernel, 1, 'k', 1)))



cv2.imshow('restored_image', restored_image)
cv2.waitKey(0)