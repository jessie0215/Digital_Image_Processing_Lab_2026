import cv2
import noiseGen
import numpy as np
import matplotlib.pyplot as plt

INPUT_IMAGE = "input.tif"
TITLES = ["original image", "Adding Gaussian Noise", "Adding Pepper Noise", "Adding Salt Noise", "Adding Both Pepper & Salt Noise"]

def show_img(ax, img, title):
    ax.imshow(img, cmap='gray', interpolation='nearest')
    ax.set_title(title)
    ax.axis('off')

def main():
    try:
        # read the image
        img_raw = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED)
        img = noiseGen.normalize_to_uint8(img_raw) 

        # obtain the image corrupted with Gaussian noise
        corruptedimage_Gaussian = noiseGen.addGaussianNoise(img,0,20)
        cv2.imwrite("out_Gaussian.tif", corruptedimage_Gaussian)
        print("Adding Gaussian Noise Successfully, Please Check out_Gaussian.tif")

        # obtain the image corrupted with pepper noise
        corruptedimage_Pepper = noiseGen.addImpulseNoise(img,0,0.1)
        cv2.imwrite("out_pepper.tif", corruptedimage_Pepper)
        print("Adding Pepper Noise Successfully, Please Check out_pepper.tif")

        # obtain the image corrupted with salt noise
        corruptedimage_Salt = noiseGen.addImpulseNoise(img,0.1,0)
        cv2.imwrite("out_salt.tif", corruptedimage_Salt)
        print("Adding Salt Noise Successfully, Please Check out_salt.tif")

        # obtain the image corrupted with both pepper & salt noise
        corruptedimage_PS = noiseGen.addImpulseNoise(img,0.1,0.1)
        cv2.imwrite("out_pepper_and_salt.tif", corruptedimage_PS)
        print("Adding Salt & Pepper Noise Successfully, Please Check out_pepper_and_salt.tif")


        # combine all the required images together
        fig, axes = plt.subplots(2, 3, figsize=(12, 6))

        show_img(axes[0,0], img, f"(a) {TITLES[0]}")
        show_img(axes[0,1], corruptedimage_Gaussian, f"(b) {TITLES[1]}")
        show_img(axes[0,2], corruptedimage_Pepper, f"(c) {TITLES[2]}")
        show_img(axes[1,0], corruptedimage_Salt, f"(d) {TITLES[3]}")
        show_img(axes[1,1], corruptedimage_PS, f"(e) {TITLES[4]}")
        fig.delaxes(axes[1,2])

        plt.tight_layout()
        plt.savefig("result.png", dpi=300)
        print("Plotting Finished, Please Check result.png")

    except Exception as e:
        print("Error:" + str(e))
        print("Operation Fails")
        print("Please Try Again")

if __name__ == "__main__":
    main()

