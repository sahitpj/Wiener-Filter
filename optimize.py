import cv2
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, process, process_2
from weiner import weiner_filter, pad_with, Find_k, unpad
import numpy as np

def optimize_1(imagepath_list):
    k_list = []
    for imagepath in imagepath_list:
        k_values = np.linspace(0, 0.2, num=20)
        scores = []
        l = 0
        best_k = 0
        for i in xrange(len(k_values)):
            score = process(imagepath, k_values[i])
            scores.append(score)
            if score > l:
                l = score
                best_k = k_values[i]
            print 1
        # plt.plot(k_values, scores)
        # plt.show()
        # print 'best k value  - ', best_k
        k_list.append(best_k)
    return sum(k_list)/len(k_list)
        

def optimize_2(kernel_size, imagepath_list):
    threshold = 40
    k_values = []
    for imagepath in imagepath_list:
        im = cv2.imread(imagepath, 0)[:101, :101] #to produe k of 101x101
        noise = gaussianNoise(im, 20)
        k = Find_k(im, noise)
        if process_2(imagepath, k) > threshold:
            k_values.append(k)
    return sum(k_values)/len(k_values)



    