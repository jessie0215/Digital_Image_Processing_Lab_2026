# Proj 03-03 Spatial Filtering
# output = spatialFiltering(input, mask); (2-D convolution)
# input: a 2-D grayscale image data, type np.float32, range 0~1
# output: a 2-D grayscale image data, type np.float32, range 0~1
# mask: a 2-D mask, type np.float32
# 可使用內建的 np.pad()
# mask size 可自訂

import numpy as np
import cv2

INPUT_IMAGE = "input.tif"
KERNEL_SIZE = 3 # fix mask size as 3 * 3


def normalization(img):
    img = img.astype(np.float32)
    maxval = img.max()
    minval = img.min()
    if maxval - minval == 0:
        return np.zeros_like(img, dtype=np.float32)
    return (img - minval) / (maxval-minval)

def spatialFiltering(input, mask):
    """
    input: a padded image for convolution
    mask: a 2-D array for convulution 
    """
    
    a = KERNEL_SIZE // 2
    h,w = input.shape

    transformedimage = np.zeros((h - 2*a, w - 2*a), dtype=np.float32)
    
    for i in range(a,h-a):
        for j in range(a,w-a):
            conv_sum = 0

            for s in range(-a, a+1):
                for t in range(-a, a+1):
                    conv_sum += mask[s+a,t+a] * input[i-s, j-t]
            
            transformedimage[i-a,j-a] = np.float32(conv_sum)

    return transformedimage        


def main():
    try:
        # prompt user to input mask
        mask_raw = input(f"Please give {KERNEL_SIZE*KERNEL_SIZE} numbers for the mask: ").split()
        mask = np.array(list(map(np.float32, mask_raw))).reshape(KERNEL_SIZE,KERNEL_SIZE)
        
        # read the image
        img = cv2.imread(INPUT_IMAGE,cv2.IMREAD_UNCHANGED)
        img = normalization(img)

        # padding zeros
        pad = KERNEL_SIZE // 2 
        img = np.pad(img, pad, mode= "constant")

        # applying spatial filtering
        output = spatialFiltering(img,mask)
        output = np.clip(output,0.0,1.0)

        # write to output file
        cv2.imwrite("out_spatialfilter.tif", output)

        # np.savetxt("input.txt", img, fmt = "%.6f")
        # np.savetxt("output.txt", output, fmt="%.6f")

        print("Finish Processing")
        print("Please Check out_spatialfilter.tif")
        
    except Exception as e:
        print("Error" + str(e))
        print("Spatial Filtering Fails")
        print("Please Try Again")


if __name__ == "__main__":
    main()