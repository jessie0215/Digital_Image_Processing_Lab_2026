import cv2
import numpy as np
import LowPass
import matplotlib.pyplot as plt

INPUT_IMAGE = "input.tif"
D0_list =[10,30,60,160,460]

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

def init():
    # preprocessing
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED) 
    img = img.astype(np.float32) / 255.0
    pad_img = LowPass.mirrorPad(img)
    shift_img = LowPass.shiftSpectrum(pad_img)
    print("Image Centered")

    # performing DFT
    dft_img = np.fft.fft2(shift_img)
    print("DFT Performed")

    return img, dft_img

def performLowPassFiltering(D0, img, dft_img):
    try:
        # prepare filter
        M,N = dft_img.shape
        filter = LowPass.myGLPF(D0, M, N)

        # perform filtering
        filtered_spectrum = dft_img * filter
        print("Filtering Performed")

        # peform IDFT
        idft_image = np.real(np.fft.ifft2(filtered_spectrum))
        print("IDFT Performed")

        # postprocessing
        shift_output = LowPass.shiftSpectrum(idft_image)
        X,Y = img.shape
        cropped_img = shift_output[:X , :Y]

        display = display_adjustment(cropped_img)

        cv2.imwrite(f"out_{D0}.tif", display)
        print(f"final result generate, please check out_{D0}.tif")

        return display

    except Exception as e:
        print("Error:" + str(e))
        print("Transformation Fails")
        print("Please Try Again")
        

def main():
    try:
        fig, axes = plt.subplots(2, 3, figsize=(12, 6))
        img, dft_img = init()
        result_set = [img]
        for D0 in D0_list:
            result_set.append(performLowPassFiltering(D0, img, dft_img))
        
        for i, img in enumerate(result_set):
            if i == 0:
                title = "original"
            else:
                title = f"D0 = {D0_list[i-1]}"
            show_img(axes[i//3, i%3], img, title)

        plt.tight_layout()
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

   