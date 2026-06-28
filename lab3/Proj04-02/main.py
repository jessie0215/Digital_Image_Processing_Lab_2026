# 註 1：輸出的 spectrum 請記得 centered
# 註 2：基於計算效率的考量，可使用 fft2()（MATLAB）／numpy.fft.fft2()（Python）計算，
# 然不可使用 fftshift()（MATLAB）／numpy.fft.fftshift()（Python）進行 centered，這部分請自行實作

import cv2
import numpy as np
import matplotlib.pyplot as plt

INPUT_IMAGE = "input.tif"

def show_img(ax, img, title):
    ax.imshow(img, cmap='gray', interpolation='nearest')
    ax.set_title(title)
    ax.axis('off')

def display_adjustment(img, iscomplex=False):
    if iscomplex:
        magnitude = np.abs(img)
        log_spectrum = np.log(1 + magnitude)
        minv = log_spectrum.min()
        maxv = log_spectrum.max()
        if maxv == minv:
            return np.zeros_like(log_spectrum, dtype=np.uint8)
        norm_spectrum = (log_spectrum - minv) / (maxv - minv)
        return (norm_spectrum * 255).astype(np.uint8)
    else:
        img = img.astype(np.float32)
        minv = img.min()
        maxv = img.max()
        if maxv == minv:
            return np.zeros_like(img, dtype=np.uint8)
        display = (img - minv) / (maxv - minv)
        return (display * 255).astype(np.uint8)
    

def shiftSpectrum(input):
    M, N = input.shape
    x = np.arange(M).reshape(M, 1)
    y = np.arange(N).reshape(1, N)
    shift = (-1) ** (x + y)
    output = input * shift
    return output

def main():
    try:

        # preprocessing
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED) 
        img = img.astype(np.float32) / 255.0

        # center image
        shifted_img = shiftSpectrum(img)

        # compute DFT
        spectrum = np.fft.fft2(shifted_img)
        display_img = display_adjustment(spectrum, True)
        cv2.imwrite("spectrum.tif", display_img)
        print("spectrum image saved, please check spectrum.tif")

        # compute mean via 2 ways
        direct_mean = np.mean(img)

        M,N = spectrum.shape
        spectrum_mean = np.real(spectrum[M // 2, N // 2]) / (M * N)

        # output
        print("mean_direct =", direct_mean)
        print("mean_from_spectrum =", spectrum_mean)

        # put all the required images together
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        show_img(axes[0], img, "(a) Original")
        show_img(axes[1], display_img, "(b) Spectrum")
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig("result.png", dpi=300)
        print("result saved, please check result.png")

        print("=" * 40)
        print("All Tasks Done")


    except Exception as e:
        print("Error:" + str(e))
        print("Operation Fails")
        print("Please Try Again")


if __name__ == "__main__":
    main()