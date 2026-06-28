### Python 請將圖片轉為 float32 並正規化至 range 0~1
# output = logTransform(input, c)  (Eq. (3.2-2) [4/e Eq. (3-4)])
# output = powerlawTransform(input, c, r) ; (Eq. (3.2-3) [4/e Eq. (3-5)])
# input: a 2-D grayscale image data, type np.float32 (Python), range 0~1 
# output: a 2-D grayscale image data, type  np.float32 (Python),range 0~1 
# c: a constant
# r: gamma value used in power law transformation, type np.float32 (Python) 
# 不可使用 skimage.exposure.adjust_log(), skimage.exposure.adjust_gamma()

import numpy as np

def logTransform(input,c):
    return c * np.log(1+input)

def powerlawTransform(input, c, r):
    return c* np.power(input,r)
