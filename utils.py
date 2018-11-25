import numpy as np


def Gaussian(size, stddev):
    s, k = stddev, size #generates gaussian of size 2k+1 x 2k+1
    probs = [np.exp(-z*z/(2*s*s))/np.sqrt(2*np.pi*s*s) for z in range(-k,k+1)] 
    l = np.outer(probs, probs)
    gaussian = l/np.sum(l)
    return gaussian


def convolution2d(image, kernel, noise):
    m, n = kernel.shape
    if (m == n):
        y, x = image.shape
        y = y - m + 1
        x = x - m + 1
        new_image = np.zeros((y,x))
        for i in range(y):
            for j in range(x):
                new_image[i][j] = np.sum(image[i:i+m, j:j+m]*kernel) + noise
    return new_image/255

def gaussianNoise(image, stddev):
    row,col = image.shape
    mean = 0
    var = stddev**2
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col))
    gauss = gauss.reshape(row,col)
    return gauss/255


def imageResize(image):
    n = 0
    if image.shape[0] > image.shape[1]:
        if image.shape[1]%2 == 0:
            n = image.shape[1] - 1
        else:
            n = image.shape[1]
    else:
        if image.shape[0]%2 == 0:
            n = image.shape[0] - 1
        else:
            n = image.shape[0]
    return image[:n, :n]
    
def image_rotate(restored_image):
    r = restored_image.shape[0]%2
    l = restored_image.shape[0]-r
    replaced_image = np.ones((l, l))
    k = restored_image.shape[0]/2
    replaced_image[ :k,  :k] = restored_image[k:l, k:l]
    replaced_image[ :k, k:l] = restored_image[k:l,  :k]
    replaced_image[k:l,  :k] = restored_image[ :k, k:l]
    replaced_image[k:l, k:l] = restored_image[ :k,  :k]
    return replaced_image