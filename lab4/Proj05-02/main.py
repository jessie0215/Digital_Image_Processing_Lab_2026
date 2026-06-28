import cv2
import medianFilter as mf
import numpy as np
import matplotlib.pyplot as plt

INPUT_IMAGE = "input.tif"
TITLES = ["original image", "Adding Pepper & Salt Noise", "Applying Median Filtering"]

def show_img(ax, img, title):
    ax.imshow(img, cmap='gray', interpolation='nearest')
    ax.set_title(title)
    ax.axis('off')

def main():
    try:
        # read the image
        img_raw = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED)
        img = mf.normalize_to_uint8(img_raw) 

        # obtain the image corrupted with both pepper & salt noise
        corruptedimg= mf.addImpulseNoise(img,0.2,0.2)
        cv2.imwrite("out_pepper_and_salt.tif", corruptedimg)
        print("Adding Salt & Pepper Noise Successfully, Please Check out_pepper_and_salt.tif")

        # apply median filtering
        restored_img = mf.myMedianFilter(corruptedimg)
        cv2.imwrite("restored_img.tif",restored_img)
        print("Apply Median Filtering Successfully, Please Check restored_img.tif")

        # combine all the required images together
        fig, axes = plt.subplots(1, 3, figsize=(12, 6))

        show_img(axes[0], img, f"(a) {TITLES[0]}")
        show_img(axes[1], corruptedimg, f"(b) {TITLES[1]}")
        show_img(axes[2], restored_img, f"(c) {TITLES[2]}")

        plt.tight_layout()
        plt.savefig("result.png", dpi=300)
        print("Plotting Finished, Please Check result.png")

    except Exception as e:
        print("Error:" + str(e))
        print("Operation Fails")
        print("Please Try Again")

if __name__ == "__main__":
    main()

