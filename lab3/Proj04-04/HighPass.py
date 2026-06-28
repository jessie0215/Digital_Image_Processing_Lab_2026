# D0: variable of Gaussian Highpass Filtering, dtype=np.float32 (see Eq. (4.9-4) [第四版課本
# Eq. (4-120)])
# M, N: size of the filter (M×N), type int
# output: 2-D numpy array (GHPF), dtype=np.float32
# 註 1：假設 filter 的中心點在正中央
# 註 2：基於計算效率的考量，可使用 fft2()（MATLAB）／numpy.fft.fft2()（Python）計算，
# 然不可使用 fftshift()（MATLAB）／numpy.fft.fftshift()（Python）進行 centered，這部分請自行實作
import numpy as np


def zeroPad(input):
    M, N = input.shape
    padded = np.zeros((2*M, 2*N), dtype=input.dtype)
    padded[:M, :N] = input
    return padded


def shiftSpectrum(input):
    M, N = input.shape
    x = np.arange(M).reshape(M, 1)
    y = np.arange(N).reshape(1, N)
    shift = (-1) ** (x + y)
    output = input * shift
    return output


def myGHPF(D0, M, N):
    u = np.arange(M, dtype=np.float32)
    v = np.arange(N, dtype=np.float32)

    u = u.reshape(M, 1)
    v = v.reshape(1, N)

    D_squared = (u - M/2)**2 + (v - N/2)**2

    H = 1 - np.exp(-D_squared / (2 * (D0**2)))

    return H.astype(np.float32)