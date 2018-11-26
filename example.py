import cv2
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, image_rotate, imageRemap, ImageScale
from weiner import weiner_filter,  pad_with, unpad
import numpy as np
from optimize import optimize

# im = imageResize(cv2.imread("trailset/image_test.jpg", 0))
im = imageResize(cv2.imread("dataset/ant/image_0001.jpg", 0))

gaussian_kernel = Gaussian(5, 1)
gaussian_blur = convolution2d(im, gaussian_kernel, 0)

im = unpad(im, 5)
noise = gaussianNoise(im, 20)
assert(gaussian_blur.shape == noise.shape)
noisy_image = gaussian_blur + noise

k = np.ones((im.shape[0], im.shape[0]))

F1 = weiner_filter(noisy_image)
method = 'FBDB'
r = np.real(F1.filter(gaussian_kernel, method, k))
restored_image = ImageScale(imageRemap(method, r))


score = F1.metric(restored_image, im)
print 'restoration score -', score


cv2.imshow('m1', restored_image)
cv2.waitKey(0)
# optimize(1, "trailset/image_test.jpg")
if method == 'k':
    optimize(1, "dataset/ant/image_0001.jpg")