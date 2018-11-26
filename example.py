import cv2
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, image_rotate
from weiner import weiner_filter,  pad_with
import numpy as np
from optimize import optimize

im = imageResize(cv2.imread("trailset/image_test.jpg", 0))


gaussian_kernel = Gaussian(5, 1)
p = convolution2d(im, gaussian_kernel, 0)
gaussian_blur = np.pad(p, (im.shape[0]-p.shape[0])/2, pad_with, padder=1)
noise = gaussianNoise(im, 20)
assert(gaussian_blur.shape == noise.shape)
noisy_image = gaussian_blur + noise
F1 = weiner_filter(noisy_image)
r = np.real(F1.filter(gaussian_kernel, 'k', 1))
restored_image = (image_rotate(r))


score = F1.metric(restored_image, im)
print 'restoration score -', score

# cv2.imshow('m1', restored_image)
# cv2.waitKey(0)
optimize(1, "trailset/image_test.jpg")