# D0: variable of Gaussian Lowpass Filtering, type single (see Eq. (4.8-7) [第四版課本 Eq. (4-116)])
# M, N: size of the filter (M×N), type int
# output: a 2-D GLPF, type single
# 註 1：假設 filter 的中心點在正中央
# 註 2：基於計算效率的考量，可使用 fft2()（MATLAB）／numpy.fft.fft2()（Python）計算，
# 然不可使用 fftshift()（MATLAB）／numpy.fft.fftshift()（Python）進行 centered，這部分請自行實作
import numpy as np
import cv2


def mirrorPad(img):
    M, N = img.shape
    padded = cv2.copyMakeBorder(
        img,
        0, M,      # 上下
        0, N,      # 左右
        borderType=cv2.BORDER_REFLECT
    )
    return padded


def shiftSpectrum(input):
    M, N = input.shape
    x = np.arange(M).reshape(M, 1)
    y = np.arange(N).reshape(1, N)
    shift = (-1) ** (x + y)
    output = input * shift
    return output


def myGLPF(D0, M, N):
    u = np.arange(M, dtype=np.float32)
    v = np.arange(N, dtype=np.float32)

    u = u.reshape(M, 1)
    v = v.reshape(1, N)

    D_squared = (u - M/2)**2 + (v - N/2)**2

    H = np.exp(-D_squared / (2 * (D0**2)))

    return H.astype(np.float32)