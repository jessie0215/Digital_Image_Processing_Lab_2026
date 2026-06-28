# output_s = myMedianFilter(input_s)
# input_s & output_s: 2-D numpy array in spatial domain, dtype=np.uint8, range 0~255
import numpy as np

KERNEL_SIZE = 3

def normalize_to_uint8(img):
    img = img.astype(np.float32)

    min_val = np.min(img)
    max_val = np.max(img)

    if max_val == min_val:
        return np.zeros_like(img, dtype=np.uint8)

    img = (img - min_val) / (max_val - min_val) * 255
    return img.astype(np.uint8)


# Noise Generator From Proj05-01
def addImpulseNoise(input_s, Ps, Pp):
    output_s = input_s.copy()

    rand = np.random.rand(*input_s.shape)

    output_s[rand < Pp] = 0

    output_s[(rand >= Pp) & (rand < Pp + Ps)] = 255

    return output_s.astype(np.uint8)


def myMedianFilter(input_s):
    
    a = KERNEL_SIZE // 2 # padding size
    img_pad = np.pad(input_s, a, mode= "reflect")
    h,w = img_pad.shape
    transformedimage = np.zeros((input_s.shape), dtype=np.uint8)
    
    for i in range(a,h-a):
        for j in range(a,w-a):
            ele = []

            for s in range(-a, a+1):
                for t in range(-a, a+1):
                    ele.append(img_pad[i+s,j+t])
            ele.sort()
            transformedimage[i-a,j-a] = ele[KERNEL_SIZE * KERNEL_SIZE // 2]

    return transformedimage        
