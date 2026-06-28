# Zooming and Shrinking Images by Bilinear Interpolation
import numpy as np


def resizeImage_bilinear (originalImage, scalingFactor):
    """
    originalImage: 還沒 resize 的原影像
    scalingFactor: resize 的 scale (例如要放大為兩倍: 2; 縮小為一半: 1/2) 
    resizedImage: resize 後的影像
    """

    # create a new image(numpy array) with adjusted size
    scale = float(scalingFactor)

    h,w = originalImage.shape

    new_h = max(1, round(h * scale))
    new_w = max(1, round(w * scale))

    resizedImage = np.empty((new_h,new_w), dtype=originalImage.dtype)

    ## preprocessing

    # compute the mapping coordinate for each pixel
    src_ys = np.arange(new_h) / scale
    src_xs = np.arange(new_w) / scale

    # compute the coordinate of four neighbors
    y1s = np.floor(src_ys).astype(int)
    x1s = np.floor(src_xs).astype(int)
    y2s = np.minimum(y1s + 1, h - 1)
    x2s = np.minimum(x1s + 1, w - 1)

    # compute the difference on both axes for interpolation
    dys = src_ys - y1s
    dxs = src_xs - x1s
    
    # main loop to calculate bilinear interpolation result for each pixel
    for y in range(new_h):
        
        if y % 500 == 0:
            print(f"processing row {y}..")
        
        for x in range(new_w):

            y1 = y1s[y]
            x1 = x1s[x]

            y2 = y2s[y]
            x2 = x2s[x]

            dx = dxs[x]
            dy = dys[y]

            # the formula of interpolation
            new_value = (1-dx) * ((1-dy)* originalImage[y1,x1] + dy * originalImage[y2,x1])\
                        + dx * ((1-dy) * originalImage[y1,x2] + dy * originalImage[y2,x2])
            
            # fill in the computed new value
            resizedImage[y, x] = np.clip(round(new_value), 0, 255)

    return resizedImage