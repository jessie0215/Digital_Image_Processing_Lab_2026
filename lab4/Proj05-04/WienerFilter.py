# output_f, H = addMotionBlur(input_f, T, a, b)
# output_f = wienerFiltering(input_f, H, K)
# input_f & output_f: 2-D numpy array in frequency domain (centered), dtype=np.complex64
# H: 2-D numpy array (motion blur degradation function), dtype=np.complex64
# T & a & b: motion blur parameters (見 Eq. 5.6-11 [第四版課本 Eq. 5-77])
# K: Wiener filter parameter (見 Eq. 5.8-6 [第四版課本 Eq. 5-85])

import numpy as np

def shiftSpectrum(input):
    M, N = input.shape
    x = np.arange(M).reshape(M, 1)
    y = np.arange(N).reshape(1, N)
    shift = (-1) ** (x + y)
    output = input * shift
    return output

def normalize_to_float32(img):
    img = img.astype(np.float32)

    min_val = np.min(img)
    max_val = np.max(img)

    if max_val == min_val:
        return np.zeros_like(img, dtype=np.float32)

    img = (img - min_val) / (max_val - min_val) 
    return img.astype(np.float32)

def adjustment(img):
    magnitude = np.abs(img)
    log_spectrum = np.log(1 + magnitude)
    minv = log_spectrum.min()
    maxv = log_spectrum.max()
    if maxv == minv:
        return np.zeros_like(log_spectrum, dtype=np.uint8)
    norm_spectrum = (log_spectrum - minv) / (maxv - minv)
    return (norm_spectrum * 255).astype(np.uint8)



def addGaussianNoise(input_s, mu, sigma):
    input_float = input_s.astype(np.float32)

    noise = np.random.normal(mu, sigma, input_s.shape)

    noisy_img = input_float + noise

    output_s = np.clip(noisy_img, 0, 255)

    return output_s.astype(np.float32)

def computePSNR(input1_s, input2_s):
    input1_s = input1_s.astype(np.float32)
    input2_s = input2_s.astype(np.float32)

    M, N = input1_s.shape
    f_peak = 255.0

    sse = np.sum((input1_s - input2_s) ** 2)

    if sse == 0:
        return float("inf")

    psnr = 10 * np.log10((M * N * (f_peak ** 2)) / sse)

    return psnr

def addMotionBlur(input_f, T, a, b):
    M, N = input_f.shape

    # centered frequency coordinates
    u = np.arange(M).reshape(M, 1) - M / 2
    v = np.arange(N).reshape(1, N) - N / 2

    # pi * (u*a + v*b)
    term = np.pi * (u * a + v * b)

    H = np.zeros((M, N), dtype=np.complex64)

    # avoid division by zero when term == 0
    mask = term != 0 # a boolean array record whether a zero division is occuring

    # if no zero division -> compute through the formula
    H[mask] = ((T / term[mask])* np.sin(term[mask])* np.exp(-1j * term[mask]))

    # limit value when term approaches 0 is T
    H[~mask] = T

    output_f = input_f * H

    return output_f.astype(np.complex64), H.astype(np.complex64)

def wienerFiltering(input_f, H, K):

    H_abs_square = np.abs(H) ** 2

    output_f = (np.conj(H) / (H_abs_square + K)) * input_f

    return output_f.astype(np.complex64)


