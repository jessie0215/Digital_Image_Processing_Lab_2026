import cv2
import DFT
import numpy as np
import os, sys
sys.path.append(os.path.abspath("../Proj04-03"))
import LowPass
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

def main():
    try:

        is_pad = input("Please specifiy if zero padding is needed (Y/N): ") 

        # preprocessing
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED) 
        img = img.astype(np.float32) / 255.0
        img = cv2.resize(img, (256,256))

        # zero padding
        if is_pad == 'Y' or is_pad == 'y':
            zero_pad_img = DFT.zeroPad(img)
            
            display_zero_pad = display_adjustment(zero_pad_img)
            cv2.imwrite("zero_pad.tif", display_zero_pad)
            print("zero padding finished",end = ", ")
            print("please check zero_pad.tif")


        # multiplied by (-1) ^ (x+y)
        if is_pad == 'Y' or is_pad == 'y':
            shifted_img = DFT.shiftSpectrum(zero_pad_img)
        else: 
            shifted_img = DFT.shiftSpectrum(img)
        display_shifted_img = np.clip(shifted_img, 0, None)
        display_shifted_img = (display_shifted_img * 255).astype(np.uint8)
        cv2.imwrite("shifted_img.tif", display_shifted_img)
        print("successfully multiplied by (-1)^(x+y)",end = ", ")
        print("please check shifted_img.tif")

        # performing DFT
        dft_img = DFT.myDFT2(shifted_img)

        display_spectrum = display_adjustment(dft_img, True)
        cv2.imwrite("spectrum.tif", display_spectrum)
        print("successfully performing DFT",end = ", ")
        print("please check spectrum.tif")

        # prepare filter
        H = LowPass.myGLPF(30, *shifted_img.shape)
        
        display_H = display_adjustment(H)
        cv2.imwrite("filter.tif", display_H)
        print("Gaussian LPF generated",end = ", ")
        print("please check filter.tif")

        # perform frequency domain filtering
        filtered_dft = dft_img  * H
        
        display_filtered = display_adjustment(filtered_dft, True)
        cv2.imwrite("filtered_spectrum.tif", display_filtered)
        print("frequency domain filtering finished",end = ", ")
        print("please check filtered_spectrum.tif")

        # performing IDFT and multiplied by (-1) ^ (x+y)
        recovered = DFT.myIDFT2(filtered_dft)
        recovered = DFT.shiftSpectrum(recovered)
        print("IDFT finished")


        # cropping if zero padding is applied
        if is_pad == 'Y' or is_pad == 'y':
            display_recovered = display_adjustment(recovered)
            cv2.imwrite("filtered_raw.tif", display_recovered)
            print("raw filtered image generated",end =", ")
            print("please check filter_raw.tif")

            recovered = recovered[:256, :256]
            display_crop = display_adjustment(recovered)
            cv2.imwrite("output_zero_pad.tif", display_crop)
            print("final output generated",end = ", ")
            print("please check output_zero_pad.tif")

        else:
            display = display_adjustment(recovered)
            cv2.imwrite("output.tif", display)
            print("final output generated" ,end = ", ")
            print("please check output.tif")

        # put all images together if zero padding is applied
        if is_pad == "Y" or is_pad == "y":
            fig, axes = plt.subplots(2, 4, figsize=(12, 6))

            show_img(axes[0,0], img, "(a) Original")
            show_img(axes[0,1], display_zero_pad, "(b) Padded")
            show_img(axes[0,2], display_shifted_img, "(c) Shifted")
            show_img(axes[0,3], display_spectrum, "(d) Spectrum")
            show_img(axes[1,0], display_H, "(e) Filter")
            show_img(axes[1,1], display_filtered, "(f) Filtered Spectrum")
            show_img(axes[1,2], display_recovered, "(g) Recovered")
            show_img(axes[1,3], display_crop, "(h) Final Output")

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