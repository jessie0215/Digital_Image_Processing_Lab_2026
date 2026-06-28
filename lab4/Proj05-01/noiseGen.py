# output_s = addGaussianNoise(input_s, mu, sigma)
# output_s = addImpulseNoise(input_s, Ps, Pp)
# input_s & output_s: 2-D numpy array in spatial domain, dtype=np.uint8, range 0~255
# mu, sigma: parameters of gaussian noise (c.f. 4/e, eq. 5-3)
# Ps, Pp: parameters of salt noise and pepper noise respectively (c.f. 4/e, eq. 5-16)
import numpy as np

def normalize_to_uint8(img):
    img = img.astype(np.float32)

    min_val = np.min(img)
    max_val = np.max(img)

    if max_val == min_val:
        return np.zeros_like(img, dtype=np.uint8)

    img = (img - min_val) / (max_val - min_val) * 255
    return img.astype(np.uint8)


def addGaussianNoise(input_s, mu, sigma):
    input_float = input_s.astype(np.float32)

    noise = np.random.normal(mu, sigma, input_s.shape)

    noisy_img = input_float + noise

    output_s = normalize_to_uint8(noisy_img)

    return output_s

def addImpulseNoise(input_s, Ps, Pp):
    output_s = input_s.copy()

    rand = np.random.rand(*input_s.shape)

    output_s[rand < Pp] = 0

    output_s[(rand >= Pp) & (rand < Pp + Ps)] = 255

    return output_s.astype(np.uint8)