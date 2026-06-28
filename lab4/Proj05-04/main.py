import cv2
import WienerFilter as wf
import numpy as np
import matplotlib.pyplot as plt

INPUT_IMAGE = "input.tif"
TITLES = ["original image", "Adding Motion Blur", "Adding Noise on (b)", "Wiener Filtering (K = 0.1)","Wiener Filtering (K = 0.01)","Wiener Filtering (K = 0.001)"]
Ks = [0.1, 0.01, 0.001]

def show_img(ax, img, title):
    ax.imshow(img, cmap='gray', interpolation='nearest')
    ax.set_title(title)
    ax.axis('off')

def to_frequency_domain(img):
    shifted_img = wf.shiftSpectrum(img)
    return np.fft.fft2(shifted_img).astype(np.complex64)

def to_spatial_domain(img):
    img_s = np.real(np.fft.ifft2(img)).astype(np.float32)
    return wf.shiftSpectrum(img_s)


def main():
    try:
        # read the image
        img_raw = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED)
        img = img_raw.astype(np.float32)

        # obtain the frequency spectrum of input image
        spectrum = to_frequency_domain (img)
        print("Transfer To Frequency Domain Successfully")

        # applying motion blur degradation and transfer back to spatial domain
        degraded_img_f , H = wf.addMotionBlur(spectrum, 1, 0.1, 0.1)
        degraded_img_s = to_spatial_domain(degraded_img_f)
        display_degraded_img_s = np.clip(degraded_img_s, 0, 255).astype(np.uint8)
        cv2.imwrite("out_degraded.tif", display_degraded_img_s)
        print("Adding Motion Blur Successfully, Please Check out_degraded.tif")
        
        # adding Gaussain Noise
        degraded_noisy_img_s = wf.addGaussianNoise(degraded_img_s, 0, np.sqrt(10))
        display_degraded_noisy_img_s = np.clip(degraded_noisy_img_s, 0, 255).astype(np.uint8)
        cv2.imwrite("out_noisy.tif", display_degraded_noisy_img_s)
        print("Adding Gaussian Noise Successfully, Please Check out_noisy.tif") 


        # applying Wiener Filtering
        degraded_noisy_img_f = to_frequency_domain(degraded_noisy_img_s)
        display_restored_img_s = []

        for i, k in enumerate(Ks):
            restore_img = wf.wienerFiltering(degraded_noisy_img_f, H, k)
            restored_img_s = to_spatial_domain(restore_img)

            # for displaying purpose -> turn back to uint8
            display_restored_img_s.append(np.clip(restored_img_s, 0, 255).astype(np.uint8))
            cv2.imwrite(f"out_K{i+1}.tif", display_restored_img_s[i]) 
            print(f"Applying Wiener Filtering on K = {k}, Please Check out_K{i+1}")

            psnr = wf.computePSNR(img, restored_img_s)
            print(f"[OUTPUT] PSNR between input and restored image = {psnr} dB")

        # combine all the required images together
        fig, axes = plt.subplots(2, 3, figsize=(12, 6))
        
        show_img(axes[0,0], img, f"(a) {TITLES[0]}")
        show_img(axes[0,1], display_degraded_img_s, f"(b) {TITLES[1]}")
        show_img(axes[0,2], display_degraded_noisy_img_s, f"(c) {TITLES[2]}")
        show_img(axes[1,0], display_restored_img_s[0], f"(d) {TITLES[3]}")
        show_img(axes[1,1], display_restored_img_s[1], f"(e) {TITLES[4]}")
        show_img(axes[1,2], display_restored_img_s[2], f"(f) {TITLES[5]}")

        plt.tight_layout()
        plt.savefig("result.png", dpi=300)
        print("Plotting Finished, Please Check result.png")

    except Exception as e:
        print("Error:" + str(e))
        print("Operation Fails")
        print("Please Try Again")

if __name__ == "__main__":
    main()

