import cv2, sys
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, image_rotate
from weiner import weiner_filter, pad_with
from optimize import optimize
import numpy as np

imagepath = str(sys.argv[1])
kernelsize = 5
if len(sys.argv[1:]) != 1:
    kernelsize = int(sys.argv[2])


im = imageResize(cv2.imread(imagepath, 0))
# cv2.imshow('Original Image', im)
# cv2.waitKey(0)
print ''
print 'Using Gaussian Kernel of size 5 as blur (default) with stddev = 1'
print 'In order to change it, input it as the second command line argument'
print ''

gaussian_kernel = Gaussian(kernelsize, 1)
p = convolution2d(im, gaussian_kernel, 0)
gaussian_blur = np.pad(p, (im.shape[0]-p.shape[0])/2, pad_with, padder=1)
# cv2.imshow('Blurred Image', gaussian_blur)
# cv2.waitKey(0)

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
optimize(1, "trailset/image_test.jpg")
