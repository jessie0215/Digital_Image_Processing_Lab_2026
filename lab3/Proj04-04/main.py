import cv2
import numpy as np
import HighPass
import matplotlib.pyplot as plt

INPUT_IMAGE = "input.tif"
D0_list =[60,160]

def show_img(ax, img, title):
    ax.imshow(img, cmap='gray', interpolation='nearest')
    ax.set_title(title)
    ax.axis('off')

def init():
    try:
        # preprocessing
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED) 
        img = img.astype(np.float32)
        pad_img = HighPass.zeroPad(img)
        shift_img = HighPass.shiftSpectrum(pad_img)
        print("Image Centered")

        # performing DFT
        dft_img = np.fft.fft2(shift_img)
        print("DFT Performed")

        return img, dft_img
    
    except Exception as e:
        print("Error:" + str(e))
        print("Operation Fails")
        print("Please Try Again")

def performHighPassFiltering(D0, img, dft_img):
    try:
        # prepare filter
        M,N = dft_img.shape
        filter = HighPass.myGHPF(D0, M, N)

        # perform filtering
        filtered_spectrum = dft_img * filter
        print("Filtering Performed")

        # peform IDFT
        idft_image = np.real(np.fft.ifft2(filtered_spectrum))
        print("IDFT Performed")

        # postprocessing
        shift_output = HighPass.shiftSpectrum(idft_image)
        X,Y = img.shape
        cropped_img = shift_output[:X , :Y]

        display = np.clip(cropped_img, 0, 255).astype(np.uint8)

        cv2.imwrite(f"out_{D0}.tif", display)
        print(f"final result generate, please check out_{D0}.tif")
        return display

    except Exception as e:
        print("Error:" + str(e))
        print("Operation Fails")
        print("Please Try Again")

def main():
    try:
        img, dft_img = init()
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        for i, D0 in enumerate(D0_list):
            result = performHighPassFiltering(D0, img, dft_img)
            show_img(axes[i], result, f"D0={D0}")
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig("result.png", dpi=300)
        print("ploting finished, please check result.png")

        print("=" * 40)
        print("All Tasks Done")


    except Exception as e:
        print("Error:" + str(e))
        print("Operation Fails")
        print("Please Try Again")


if __name__ == "__main__":
    main()