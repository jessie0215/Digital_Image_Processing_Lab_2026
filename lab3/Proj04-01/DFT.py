# input: 2-D numpy array, dtype=np.float32
# output (myDFT2): 2-D numpy array, dtype=np.complex64
# output (myIDFT2): 2-D numpy array, dtype=np.float32
# 本題不可使用 fft2, fft, imfilter（MATLAB）／numpy.fft.fft2, numpy.fft.fft,  scipy.ndimage.convolve（Python）
# ：若使用 for loop 實作 DFT 會導致執行速度緩慢，因此本題統一將 input image 縮小 4 倍
#（1026×1026 → 256×256），resize 可使用內建函數（MATLAB：imresize；Python：skimage.transform.resize 或 cv2.resize）
# 報告的第(1)點要用的 Gaussian lowpass filter，請使用 Proj04-03 所寫的 function 來產生
# 註 5：input 可先轉換成 float32 type（MATLAB：im2single()；Python：img.astype(np.float32) / 255.0）
# 註 6：filter 記得要跟 input 影像一樣大
# 註 7：spectrum 請記得使用 log transform，才能得到 Fig 4.35(d) 的圖案（可參照 Ch4 p.17 的式子，
# 不過該處有更正，是「log(1+F(u,v))」，以及記得對結果 normalized）

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


def dft1d(x):
    x = np.asarray(x, dtype=np.complex64)
    N = x.shape[0]

    n = np.arange(N)
    k = n.reshape((N, 1))

    W = np.exp(-2j * np.pi * k * n / N).astype(np.complex64)
    X = W @ x

    return X.astype(np.complex64)

def myDFT2(input):

    M, N = input.shape
    temp = np.zeros((M, N), dtype=np.complex64)
    output = np.zeros((M,N), dtype=np.complex64)
    
    # 對每一列做 1D DFT
    for i in range(M):
        temp[i, :] = dft1d(input[i, :])

    # 對每一行做 1D DFT
    for j in range(N):
        output[:, j] = dft1d(temp[:, j])

    return output

def myIDFT2(input):
    M, N = input.shape

    conj_input = np.conjugate(input)
    temp = myDFT2(conj_input)
    output = np.conjugate(temp) / (M * N)

    return np.real(output).astype(np.float32)
