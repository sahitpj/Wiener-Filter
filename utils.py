import numpy as np
from weiner import weiner_filter,  pad_with, unpad
import cv2

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
    l = restored_image.shape[0]
    replaced_image = np.ones((l, l))
    k = restored_image.shape[0]/2
    replaced_image[ :k,  :k] = restored_image[k+r:l, k+r:l]
    replaced_image[ :k, k:l] = restored_image[k+r:l,  :k+r]
    replaced_image[k:l,  :k] = restored_image[ :k+r, k+r:l]
    replaced_image[k:l, k:l] = restored_image[ :k+r,  :k+r]
    return replaced_image


def process(imagepath, k_value):
    im = imageResize(cv2.imread(imagepath, 0))
    gaussian_kernel = Gaussian(5, 1)
    gaussian_blur = convolution2d(im, gaussian_kernel, 0)
    im = unpad(im, 5)
    noise = gaussianNoise(im, 20)
    assert(gaussian_blur.shape == noise.shape)
    noisy_image = gaussian_blur + noise
    k = np.ones((im.shape[0], im.shape[0]))*k_value
    F1 = weiner_filter(noisy_image)
    method = 'k'
    r = np.real(F1.filter(gaussian_kernel, method, k))
    restored_image = ImageScale(imageRemap(method, r))
    return F1.metric(restored_image, im)

def process_2(imagepath, k_value): #k value is 101x101
    im = cv2.imread(imagepath, 0)[:111, :111]
    gaussian_kernel = Gaussian(5, 1)
    gaussian_blur = convolution2d(im, gaussian_kernel, 0)
    im = unpad(im, 5) #im is size 101x101
    noise = gaussianNoise(im, 20) 
    assert(gaussian_blur.shape == noise.shape)
    noisy_image = gaussian_blur + noise
    k = k_value #k is size 101x101 from optmize
    F1 = weiner_filter(noisy_image)
    method = 'k'
    r = np.real(F1.filter(gaussian_kernel, method, k))
    restored_image = ImageScale(imageRemap(method, r))
    return F1.metric(restored_image, im) 

def condition_process(imagepath, k_value, noise_var, blur_var):
    im = imageResize(cv2.imread(imagepath, 0))[:111, :111]
    gaussian_kernel = Gaussian(5, blur_var)
    gaussian_blur = convolution2d(im, gaussian_kernel, 0)
    im = unpad(im, 5)
    noise = gaussianNoise(im, noise_var)
    assert(gaussian_blur.shape == noise.shape)
    noisy_image = gaussian_blur + noise
    k = np.ones((im.shape[0], im.shape[0]))*k_value
    F1 = weiner_filter(noisy_image)
    method = 'k'
    r = np.real(F1.filter(gaussian_kernel, method, k))
    restored_image = ImageScale(imageRemap(method, r))
    return F1.metric(restored_image, im)


def imageRemap(method, r):
    if method == 'k':
        restored_image = (image_rotate(r))
    elif method == 'FBDB':
        restored_image = r
    elif method == 'modified-FBDB':
        restored_image = r 
    elif method == 'AHFC':
        restored_image = r 
    return restored_image



def ImageScale(image):
    ma = np.amax(image)
    mi = np.amin(image)
    l = (image-mi)/(ma-mi)
    return l


