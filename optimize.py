import cv2
import matplotlib.pyplot as plt
from utils import Gaussian, convolution2d, gaussianNoise, imageResize, process
from weiner import weiner_filter, pad_with
import numpy as np

def optimize(images, imagepath):
    if images == 1:
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
        plt.plot(k_values, scores)
        plt.show()
        print 'best k value  - ', best_k
    else:
        None






    