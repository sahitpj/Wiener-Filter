import cv2
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, process
from weiner import weiner_filter, pad_with, Find_k
import numpy as np

def optimize_1(imagepath_list):
    k_list = []
    for imagepath in imagepath_list:
        k_values = np.linspace(0, 0.2, num=50)
        scores = []
        l = 0
        best_k = 0
        for i in xrange(len(k_values)):
            score = process(imagepath, k_values[i])
            scores.append(score)
            if score > l:
                l = score
                best_k = k_values[i]
        # plt.plot(k_values, scores)
        # plt.show()
        # print 'best k value  - ', best_k
        k_list.append(best_k)
    return np.mean(k_list)
        

def optimize_2(input_image, noise, imagepath_list):
    threshold = 40
    k_values = []
    for imagepath in imagepath_list:
        k = Find_k(input_image, noise)
        if process(imagepath, k) > threshold:
            k_values.append(k)
    return np.mean(k_values)
