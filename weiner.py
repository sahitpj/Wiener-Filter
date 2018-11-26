'''
WEINER FILTER

Weiner filter minimizes the mean square error between the genrated image and the original image.
Using this condition, we can find the DTFT of the impulse response of the filter, which we can then apply and take an
inverse fourirer tranform.

'''

import numpy as np
from scipy import fftpack

def unpad(image, unpad_width):
    return image[unpad_width:-unpad_width, unpad_width:-unpad_width]

def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector

def Find_k(input_image, noise):
    input_dtft = fftpack.fft2(input_image)
    Pxf = np.square(abs(input_dtft))/(input_image.shape[0]**2)
    noise_dtft = fftpack.fft2(noise)
    Pnf = np.square(abs(noise_dtft))/(noise.shape[0]**2)
    return Pxf/Pnf

class weiner_filter(object):
    def __init__(self, output_image):
        self.output_image = output_image
        self.input_image = None

    def filter(self, impulse_response, estimation, gamma):
        output_dtft = fftpack.fft2(self.output_image)
        padded_impulse = np.pad(impulse_response, (self.output_image.shape[0]-impulse_response.shape[0])/2, pad_with, padder=0 )
        Hf = fftpack.fft2(padded_impulse)
        Pyf = np.square(abs(output_dtft))/(self.output_image.shape[0]**2)
        Pyf_log = np.log10(Pyf)
        assert(Pyf.shape == Hf.shape)

        if estimation == 'k':
            Gf = np.divide(np.conjugate(Hf), (np.square(abs(Hf))+gamma))
            F_r = np.multiply(Gf, output_dtft)
            return fftpack.ifft2(F_r)
        elif estimation == 'FBDB':
            threshold = np.amin(Pyf_log) + (np.amax(Pyf_log)-np.amin(Pyf_log))*0.32 
            Pyf_max = np.multiply(Pyf, (Pyf_log<=threshold))
            Pyf_min = np.multiply(Pyf, (Pyf_log>threshold))
            Pxf = Pyf_min
            Pnf = Pyf_max
            Hf = np.divide(Pxf, Pyf)
            a = np.multiply(np.conjugate(Hf), Pxf)
            b = np.multiply(np.square(abs(Hf)), Pxf)+Pnf
            Gf = np.divide(a, b)
            F_r = np.multiply(Gf, output_dtft)
            return fftpack.ifft2(F_r)
        elif estimation == 'modified-FBDB':
            threshold = np.amin(Pyf_log) + (np.amax(Pyf_log)-np.amin(Pyf_log))*0.32 
            Pnf = np.multiply(Pyf, (Pyf_log<=threshold)) + np.multiply((Pyf[0][-1]+Pyf[-1][0]+Pyf[-1][-1])/3, (Pyf_log>threshold))
            Pxf = np.multiply(Pyf, (Pyf_log>threshold))
            Hf = np.divide(Pxf, Pyf)
            a = np.multiply(np.conjugate(Hf), Pxf)
            b = np.multiply(np.square(abs(Hf)), Pxf)+Pnf
            Gf = np.divide(a, b)
            F_r = np.multiply(Gf, output_dtft)
            return fftpack.ifft2(F_r)
        elif estimation == 'AHFC':
            Pnf = np.multiply(np.ones((Pyf.shape[0], Pyf.shape[1])), (Pyf[0][0]+Pyf[0][-1]+Pyf[-1][0]+Pyf[-1][-1])/4)
            threshold = np.amin(Pyf_log) + (np.amax(Pyf_log)-np.amin(Pyf_log))*0.32 
            Pxf = np.multiply(Pyf, (Pyf_log>threshold))
            Hf = np.divide(Pxf, Pyf)
            Gf = np.divide(np.multiply(np.conjugate(Hf), Pxf), np.multiply(np.square(abs(Hf)), Pxf)+Pnf)
            F_r = np.multiply(Gf, output_dtft)
            return fftpack.ifft2(F_r)







    def metric(self, restored_image, input_image):
        '''
        A metric we are using for the following is the signal to noise ratio (SNR) which can be defined as 

            = Spectral Density of Signal / Spectral Density of Noise

        We consider the SNR improvement which is the SNR of the input image diveded by the SNR of the restored image, which simplies to

            = Spectral Density of input noise / Spectral Density of Output noise
        '''
        a = (np.sum(np.square(abs(fftpack.fft2(self.output_image-input_image))))/(input_image.shape[0]**2))
        b = (np.sum(np.square(abs(fftpack.fft2(self.output_image-restored_image))))/(input_image.shape[0]**2))
        return 10*np.log10(a/b)


