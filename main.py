import cv2, sys
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, image_rotate
from weiner import weiner_filter, pad_with, unpad
from optimize import optimize
import numpy as np

imagepath = str(sys.argv[1])
kernelsize = 5
method = 'k'
if len(sys.argv[1:]) >= 2:
    kernelsize = int(sys.argv[2])

if len(sys.argv[1:]) >= 3:
    method = int(sys.argv[3])

im = imageResize(cv2.imread(imagepath, 0))
# cv2.imshow('Original Image', im)
# cv2.waitKey(0)
print ''
print 'Using Gaussian Kernel of size 5 as blur (default) with stddev = 1'
print 'In order to change it, input it as the second command line argument'
print ''
print ''
print 'Using k-optimization method'
print 'In order to change it, input it as the third command line argument'
print 'Available methods - FBDB and k-optimization'
print ''

gaussian_kernel = Gaussian(kernelsize, 1)
gaussian_blur = convolution2d(im, gaussian_kernel, 0)
# cv2.imshow('Blurred Image', gaussian_blur)
# cv2.waitKey(0)
im = unpad(im, kernelsize)

noise = gaussianNoise(im, 20)
assert(gaussian_blur.shape == noise.shape)
noisy_image = gaussian_blur + noise
# cv2.imshow('Noise + Blur Image', noisy_image)
# cv2.waitKey(0)

F1 = weiner_filter(noisy_image)
r = np.real(F1.filter(gaussian_kernel, 'k', 1))
restored_image = (image_rotate(r))
# cv2.imshow('Restored Image', restored_image)
# cv2.waitKey(0)


score = F1.metric(restored_image, im)
print 'restoration score -', score
print ''
if method == 'k':
    optimize(1, "trailset/image_test.jpg")
