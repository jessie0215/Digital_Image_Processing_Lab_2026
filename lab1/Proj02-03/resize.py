# Zooming and Shrinking Images by Pixel Replication
import numpy as np

def resizeImage_replication(originalImage, scalingFactor):
    """
    originalImage: 還沒 resize 的原影像
    scalingFactor: resize 的 scale (例如要放大為兩倍: 2; 縮小為一半: 1/2) 
    resizedImage: resize 後的影像
    """
    # compute the size of resized image
    scale = float(scalingFactor)

    h,w = originalImage.shape

    new_h = max(1, round(h * scale))
    new_w = max(1, round(w * scale))

    # prepare a new empty image 
    resizedImage = np.empty((new_h,new_w), dtype=originalImage.dtype)

    # preprocessing: find the nearest neighbor for each pixel
    src_rows = [min(int(i/scale), h-1) for i in range(new_h)]
    src_cols = [min(int(j/scale), w-1) for j in range(new_w)]

    # fill in each pixel with the value of its nearest neighbor from the original image
    for i in range(new_h):
        for j in range(new_w):
            # print(f"processing pixel ({i}, {j})...")
            resizedImage[i,j] = originalImage[src_rows[i], src_cols[j]]

    return resizedImage