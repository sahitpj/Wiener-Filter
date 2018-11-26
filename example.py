import cv2
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, image_rotate, imageRemap, ImageScale, process, process_2
from weiner import weiner_filter,  pad_with, unpad
import numpy as np
from optimize import optimize_1, optimize_2

# im = imageResize(cv2.imread("trailset/image_test.jpg", 0))
im = imageResize(cv2.imread("dataset/ant/image_0001.jpg", 0))[:111, :111]

gaussian_kernel = Gaussian(5, 1)
gaussian_blur = convolution2d(im, gaussian_kernel, 0) #decreases in size by 2kernel_size

im = unpad(im, 5)
noise = gaussianNoise(im, 20)
assert(gaussian_blur.shape == noise.shape)
noisy_image = gaussian_blur + noise

k = np.ones((im.shape[0], im.shape[0]))

F1 = weiner_filter(noisy_image)
method = 'k'
r = np.real(F1.filter(gaussian_kernel, method, k))
restored_image = ImageScale(imageRemap(method, r))


score = F1.metric(restored_image, im)
print 'restoration score -', score


# cv2.imshow('m1', restored_image)
# cv2.waitKey(0)
# optimize(1, "trailset/image_test.jpg")
l = []
for i in xrange(15):
    l.append('dataset/beaver/image_00'+str(i+10)+'.jpg')


if method == 'k':
    k1 = optimize_1(l)
    print 'best k by optimization 1 ', k1
    r = np.real(F1.filter(gaussian_kernel, method, k1))
    restored_image = ImageScale(imageRemap(method, r))
    score = F1.metric(restored_image, im)
    print 'restoration score for optimization 1 -', score

k2 = optimize_2(5, l) #k of 101x101
print 'best k by optimization 2 ', k2
r = np.real(F1.filter(gaussian_kernel, method, k2))
restored_image = ImageScale(imageRemap(method, r))
score = F1.metric(restored_image, im)
print 'restoration score optimization 2 -', score


# 5 images
imagepaths = ['dataset/beaver/image_0045.jpg', 'dataset/beaver/image_0035.jpg', 'dataset/ant/image_0010.jpg', 'dataset/bass/image_0010.jpg', 'dataset/brain/image_0010.jpg' ]

rest_scores_a = []
rest_scores_b = []
for i in xrange(5):
    a = process(imagepaths[i], k1)
    b = process_2(imagepaths[i], k2)
    rest_scores_a.append(a)
    rest_scores_b.append(b)

ax = plt.subplot(111)
x = range(1,6)
x_ = []
for i in xrange(1,6):
    x_.append(i-0.2)
ax.bar(x_, rest_scores_a,width=0.2,color='b',align='center')
ax.bar(x, rest_scores_b,width=0.2,color='g',align='center')
plt.show()