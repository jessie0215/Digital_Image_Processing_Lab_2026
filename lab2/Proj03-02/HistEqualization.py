# Proj03-02: Histogram Equalization
# input: a 2-D grayscale image data, type np.uint8 , range 0~255
# histVector: 1-D array contains the histogram of an image, 256 elements, type  np.float32, 整數 (不可命名為 histogram, 原因同上)
# output: a 2-D grayscale image data, type np.uint8 ,range 0~255
# T: a row(or column) vector of the transformation function, 256 elements, type np.uint8 , range 0~255

# histVector = imageHist(input); 
# [output, T] = histEqualization(input);

# histEqualization() 內必須用到自己寫的 imageHist()
# 畫 histogram 可以使用  plt.plot() ；
# 畫 transformation  function 可以使用 plt.step()

import matplotlib.pyplot as plt
import numpy as np


def imageHist(input):
    histVector = np.zeros(256, dtype=np.float32)
    
    for row in input:
        for pix in row:
            histVector[pix] += 1
    
    return histVector

def drawHistogram(h, name):
    
    plt.figure()
    plt.bar(np.arange(256), h)
    plt.title(f"Histogram of {name} image")
    plt.xlabel("Intensity Level")
    plt.ylabel("Count")
    plt.xlim([0, 255])
    plt.savefig(f"{name}_hist.png")
    plt.close()

    # print("sum prob:", np.sum(h))
    print(f"Histogram of {name} image is Plotted")
    return

def histEqualization(input):
    
    # get histogram and draw histogram
    histVector = imageHist(input)
    drawHistogram(histVector, "original")

    # normalize to probability
    total_pixel = input.shape[0] * input.shape[1]
    histVector = histVector / total_pixel

    # compute transformation function
    S = np.zeros(256, dtype=np.float32)
    S[0] = 255 * histVector[0]
    
    for i in range(1,256):
        S[i] = S[i-1] + 255 * histVector[i]

    S = np.round(S).astype(np.uint8)
    print("Transformation Function is Computed")

    # generate transformed image
    transformedImage = S[input]

    return transformedImage,S


def drawTransformation(T):
    x = np.arange(256)

    plt.figure()
    plt.step(x, T, where='mid')
    plt.title("Transformation Function")
    plt.xlabel("Input Intensity Level")
    plt.ylabel("Output Intensity Level")
    plt.xlim([0, 255])
    plt.ylim([0, 255])
    plt.savefig("transformation.png")
    plt.close()

    print("Transformation Function is Plotted")
    return
