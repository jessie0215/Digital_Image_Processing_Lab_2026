import cv2
import NotchFilter as nf
import numpy as np
import matplotlib.pyplot as plt

INPUT_IMAGE = "input.tif"
TITLES = ["original image", "Adding Sin Noise", "Spectrum of Noisy Image", "Notch Filter","Restored Image(Frequency Domain)", "Restored Image (Spatial Domain)"]

def show_img(ax, img, title):
    ax.imshow(img, cmap='gray', interpolation='nearest')
    ax.set_title(title)
    ax.axis('off')


def main():
    try:
        # read the image
        img_raw = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED)
        img = nf.normalize_to_float32(img_raw) 

        # obtain the image corrupted with Sine noise
        noisy_image = nf.addSinNoise(img,40/255, 35,35)
        cv2.imwrite("out_sinnoise.tif", noisy_image)
        print("Adding Sin Noise Successfully, Please Check out_sinnoise.tif")

        # obtain the frequency spectrum of the corrupted image
        shifted_noisy_image = nf.shiftSpectrum(noisy_image)
        spectrum = np.fft.fft2(shifted_noisy_image).astype(np.complex64)
        display_spectrum = nf.adjustment(spectrum)
        cv2.imwrite("out_spectrum.tif", display_spectrum)
        print("Transfer To Frequency Domain Successfully, Please Check out_spectrum.tif")

        # apply Notch filtering
        restored_img_f, Notch = nf.notchFiltering(spectrum, 12,35,35)
        display_restored_f = nf.adjustment(restored_img_f)
        cv2.imwrite("out_restored_f.tif", display_restored_f)
        display_Notch = (Notch * 255).astype(np.uint8)
        cv2.imwrite("out_Notch.tif", display_Notch)
        print("Applying Notch Filtering Successfully, Please Check out_restored_f.tif And out_Notch.tif")

        # obtain the restored image in spatial domain
        restored_img_s = np.real(np.fft.ifft2(restored_img_f)).astype(np.float32)
        shifted_restored_img = nf.shiftSpectrum(restored_img_s)
        shifted_restored_img = np.clip(shifted_restored_img, 0, 1).astype(np.float32)
        cv2.imwrite("out_restored_s.tif", shifted_restored_img)
        print("Transfer To Spatial Domain Successfully, Please Check out_restored_s.tif")

        # compute PSNR between input and restored image
        psnr = nf.computePSNR(img, shifted_restored_img)
        print(f"[OUTPUT] PSNR between input and restored image = {psnr} dB")

        # combine all the required images together
        fig, axes = plt.subplots(2, 3, figsize=(12, 6))

        show_img(axes[0,0], img, f"(a) {TITLES[0]}")
        show_img(axes[0,1], noisy_image, f"(b) {TITLES[1]}")
        show_img(axes[0,2], display_spectrum, f"(c) {TITLES[2]}")
        show_img(axes[1,0], display_Notch, f"(d) {TITLES[3]}")
        show_img(axes[1,1], display_restored_f, f"(e) {TITLES[4]}")
        show_img(axes[1,2], shifted_restored_img, f"(f) {TITLES[5]}")

        plt.tight_layout()
        plt.savefig("result.png", dpi=300)
        print("Plotting Finished, Please Check result.png")

    except Exception as e:
        print("Error:" + str(e))
        print("Operation Fails")
        print("Please Try Again")

if __name__ == "__main__":
    main()

