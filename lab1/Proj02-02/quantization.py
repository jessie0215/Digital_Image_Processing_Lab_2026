#  Reducing the Number of Intensity Levels in an Image
import numpy as np


def reduceIntensityLevel(originalImage, intensityLevel): 
    """
    originalImage: 還沒 quantize 的原影像
    intensityLevel: reduce 的 intensity level 數量 (2 到 256) 
    quantizedImage: intensity level quantized 後的影像
    """
    if intensityLevel == 256:
        return originalImage
    
    # compute the size of a single step e.g. level = 4  -> each step is 64  
    step = 256 // intensityLevel
    
    # create an empty image with equal size to the original image
    quantizedImage = np.empty_like(originalImage)

    h,w = originalImage.shape

    # compute the quantized value for each pixel
    for i in range(h):
        for j  in range(w):
            # new value = # of steps * size of step
            quantizedImage[i,j] = (originalImage[i,j] // step) * step

    # print(np.unique(quantizedImage))

    return quantizedImage