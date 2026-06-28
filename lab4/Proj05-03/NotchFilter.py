# output_s = addSinNoise(input_s, A, u0, v0)
# output_f, Notch = notchFiltering(input_f, D0, u0, v0)
# psnr = computePSNR(input1_s, input2_s)
# input_s & output_s: 2-D numpy array in spatial domain, dtype=np.float32, range 0~1
# input_f & output_f: 2-D numpy array in frequency domain (centered), dtype=np.complex64
# Notch: 2-D numpy array (notch reject filter), dtype=np.float32
# u0 & v0 & A: 請參考下式，其中 (M,N) 為 image size，A 為 amplitude of noise
# D0 & u0 & v0: 請參考第四版課本 eq. 5-34, 5-35，使用 ideal 版本，D0 為半徑，或參考下圖的公式說明
# psnr: Peak Signal-to-Noise Ratio between original image and restored image

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


def addSinNoise(input_s, A, u0, v0):
    input_s = input_s.astype(np.float32)

    M, N = input_s.shape

    x = np.arange(M).reshape(M, 1)
    y = np.arange(N).reshape(1, N)

    noise = A * np.sin(2 * np.pi * (u0 * x / M + v0 * y / N))

    output_s = input_s + noise
    output_s = np.clip(output_s, 0, 1)

    return output_s.astype(np.float32)

def notchFiltering(input_f, D0, u0, v0):
    M, N = input_f.shape

    u = np.arange(M).reshape(M, 1)
    v = np.arange(N).reshape(1, N)

    center_u = M / 2
    center_v = N / 2

    # distance to the positive noise frequency center: (M/2 + u0, N/2 + v0)
    D1 = np.sqrt((u - center_u - u0) ** 2 + (v - center_v - v0) ** 2)

    # distance to the negative noise frequency center: (M/2 - u0, N/2 - v0)
    D2 = np.sqrt((u - center_u + u0) ** 2 + (v - center_v + v0) ** 2)

    Notch = np.ones((M, N), dtype=np.float32)

    Notch[(D1 <= D0) | (D2 <= D0)] = 0

    output_f = input_f * Notch

    return output_f.astype(np.complex64), Notch.astype(np.float32)


def computePSNR(input1_s, input2_s):
    input1_s = input1_s.astype(np.float32)
    input2_s = input2_s.astype(np.float32)

    M, N = input1_s.shape
    f_peak = 1.0

    sse = np.sum((input1_s - input2_s) ** 2)

    if sse == 0:
        return float("inf")

    psnr = 10 * np.log10((M * N * (f_peak ** 2)) / sse)

    return psnr