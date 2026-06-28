# Proj03-04 Enhancement Using the Laplacian
# [output, scaledLaplacian] = laplacianFiltering(input, laplacianMask, scale);
# input: a 2-D grayscale image data, type np.float32, range 0~1
# output: a 2-D grayscale image data, type np.float32, range 0~1
# laplacianMask: a 2-D laplacian mask 
# scale: 𝑐 in Eq. (3.6-7)
# scaledLaplacian: a 2-D matrix of 𝑐 * [∇2𝑓(𝑥, 𝑦)] in Eq. (3.6-7), type single np.float32
# 可使用內建的 np.pad()
# laplacianFiltering() 內必須用到自己寫的 spatialFiltering()
# mask size可自訂

import SpatialFilter as SF
import numpy as np
import cv2

INPUT_IMAGE = "input.tif"
KERNEL_SIZE = 3

def selectMask(useDiagonal = False):
    global KERNEL_SIZE

    if KERNEL_SIZE == 3:
       if useDiagonal == 'Y':
            return np.array([
                [1, 1, 1],
                [1, -8, 1],
                [1, 1, 1]
            ], dtype=np.float32)
       else:
            return np.array([
                [0, 1, 0],
                [1, -4, 1],
                [0, 1, 0]
            ], dtype=np.float32)

    elif KERNEL_SIZE == 5:
        return np.array([
            [0, 0, -1, 0, 0],
            [0, 0, 16, 0, 0],
            [-1, 16, -60, 16, -1],
            [0, 0, 16, 0, 0],
            [0, 0, -1, 0, 0]
        ], dtype=np.float32) / 12.0

    elif KERNEL_SIZE == 7:
        return np.array([
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, -27, 0, 0, 0],
            [0, 0, 0, 270, 0, 0, 0],
            [2, -27, 270, -980, 270, -27, 2],
            [0, 0, 0, 270, 0, 0, 0],
            [0, 0, 0, -27, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0]
        ], dtype=np.float32) / 180.0

    else:
        raise ValueError("Only 3x3, 5x5, and 7x7 Laplacian masks are supported.")

def laplacianFiltering(input, laplacianMask, scale):

    # padding zeros
    pad = KERNEL_SIZE // 2
    paddedinput = np.pad(input, pad, mode="constant")

    # compute scaleLaplacian
    mask = scale * laplacianMask

    # call Spatial Filter
    scaledLaplacian = SF.spatialFiltering(paddedinput, mask)

    # enhancement
    transformedImage = scaledLaplacian + input

    return transformedImage, scaledLaplacian


def main():

    try:
        # prompt the user to input scale and kernel size
        scale = np.float32(input("Please input a scale for Laplacian Filter: "))
        global KERNEL_SIZE
        KERNEL_SIZE = int(input("Please specify the mask size (can be 3, 5, or 7): "))
        SF.KERNEL_SIZE = KERNEL_SIZE # make sure SF.spatialFiltering can access correct value
        useDiagonal = False
        if KERNEL_SIZE == 3:
            useDiagonal = input("Including Diagonal Terms? (Y/N) ").strip().lower()
        
        # preprocessing
        img = cv2.imread(INPUT_IMAGE,cv2.IMREAD_UNCHANGED)
        img = SF.normalization(img)

        # select corresponding laplacian mask
        laplacianMask = selectMask(useDiagonal)
    
        # laplacian filtering
        output, scaledLaplacian = laplacianFiltering(img, laplacianMask, scale)

        # write to output file
        output = np.clip(output,0.0,1.0)
        cv2.imwrite("out_scaledlaplacian.tif", scaledLaplacian)
        cv2.imwrite("out_laplacianfilter.tif", output)

        print("Finish Processing")
        print("Please Check out_scaledlaplacian.tif and out_laplacianfilter.tif")

    except Exception as e:
        print("Error" + str(e))
        print("Laplacian Filtering Fails")
        print("Please Try Again")


if __name__ == "__main__":
    main()

