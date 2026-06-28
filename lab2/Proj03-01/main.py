import numpy as np
import IntensityTransform as IntTran
import cv2

INPUT_IMAGE = "input.tif"


def normalization(img):
    img = img.astype(np.float32)
    maxval = img.max()
    minval = img.min()
    if maxval - minval == 0:
        return np.zeros_like(img, dtype=np.float32)
    return (img - minval) / (maxval-minval)

def main():
    while True:
        try:
            c = np.float32(float(input("Please Specify a constant for transformation: ")))
            r = np.float32(float(input("Please Specify the gamma parameter for power law transform: ")))
        except:
            print("Please give a floating point number")
            continue
        else:
            break
    
    print(f"Argument Given: c = {c}, r = {r}")

    print("Reading Image....")
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED)
    img = normalization(img)

    output_log = IntTran.logTransform(img,c)
    output_pow = IntTran.powerlawTransform(img,c,r)
    print("Transformation Finished")

    # print(output_log)
    # print(output_pow)

    normed_log = np.clip(output_log, 0.0, 1.0)
    normed_pow = np.clip(output_pow,0.0,1.0)
    
    print("Saving Ressult...")
    out1 = cv2.imwrite("out_log.tif", normed_log)
    out2 = cv2.imwrite("out_pow.tif", normed_pow)

    # print(f"min = {normed_log.min()}, max = {normed_log.max()}")
    # print(f"min = {normed_pow.min()}, max = {normed_pow.max()}")

    print(f"Please Check out_log.tif and out_pow.tif")


if __name__ == "__main__":
    main()