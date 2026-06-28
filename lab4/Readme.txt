Proj05-01: Noise Generators
    1. How to run the program
        - 請先確認 main.py、noiseGen.py 與輸入影像 input.tif 位於 Proj05-01 資料夾下
        - 在 Proj05-01 資料夾下執行
            python main.py
        - 程式會依序對輸入影像加入 Gaussian noise、pepper noise、salt noise，以及同時包含 pepper 和 salt 的 impulse noise
        - Gaussian noise 的參數可在 main.py 中透過 addGaussianNoise(input_s, mu, sigma) 調整
        - Impulse noise 的參數可在 main.py 中透過 addImpulseNoise(input_s, Ps, Pp) 調整，其中 Ps 為 salt noise 的機率，Pp 為 pepper noise 的機率

    2. Output Files
        - out_Gaussian.tif : 原始影像加入 Gaussian noise 後的結果。
        - out_pepper.tif : 原始影像加入 pepper noise 後的結果。
        - out_salt.tif : 原始影像加入 salt noise 後的結果。
        - out_pepper_and_salt.tif : 原始影像同時加入 pepper noise 和 salt noise 後的結果。
        - result.png : 將 original image、Adding Gaussian Noise、Adding Pepper Noise、Adding Salt Noise，以及 Adding Both Pepper & Salt Noise 組合而成的圖片

Proj05-02: Noise Reduction Using a Median Filter
    1. How to run the program
        - 請先確認 main.py、medianFilter.py 與輸入影像 input.tif 位於 Proj05-02 資料夾下
        - 在 Proj05-02 資料夾下執行
            python main.py
        - 程式會先對原始影像加入 salt-and-pepper noise，其中 Ps = 0.2、Pp = 0.2
        - 接著使用自行實作的 myMedianFilter() 對 noisy image 進行 3 x 3 median filtering

    2. Output Files
        - out_pepper_and_salt.tif : 對原始影像加入 salt-and-pepper noise 後的結果，其中 Ps = 0.2、Pp = 0.2。
        - restored_img.tif : 對 noisy image 使用 3 x 3 median filtering 後的 restored image。
        - result.png : 將 original image、加入 salt-and-pepper noise 後的 noisy image，以及 median filtering 後的 restored image 組合而成的比較圖。

Proj05-03: Periodic Noise Reduction Using a Notch Filter
    1. How to run the program
        - 請先確認 main.py、NotchFilter.py 與輸入影像 input.tif 位於 Proj05-03 資料夾下
        - 在 Proj05-03 資料夾下執行
            python main.py
        - 程式會對輸入影像加入 sinusoidal noise，並使用 notch filter 在 frequency domain 中移除週期性雜訊
        - 本次實驗使用的參數如下：
            A = 40 / 255
            u0 = 35
            v0 = 35
            D0 = 12

    2. Output
        - out_sinnoise.tif : 在原始影像上加入 sinusoidal noise 後的結果，可以觀察到明顯的週期性斜向條紋。
        - out_spectrum.tif : noisy image 經過 centered Fourier Transform 後的 frequency spectrum，可以觀察到週期性雜訊造成的對稱亮點。
        - out_Notch.tif : 使用 notchFiltering() 產生的 ideal notch reject filter，其中黑色區域代表被移除的頻率成分。
        - out_restored_f.tif : noisy spectrum 通過 Notch filter 後的 frequency domain 結果，可以看到雜訊頻率位置被濾除。
        - out_restored_s.tif : filtered frequency spectrum 經過 inverse Fourier Transform 後得到的 restored image。
        - result.png : 將原圖、加入 noise 後的影像、noisy spectrum、Notch filter、filtered spectrum 與 restored image 組合而成的圖片。
        - 執行完成後，終端機會顯示原圖與 restored image 之間的 PSNR。本次實驗結果約為：PSNR = 30.52 dB

Proj05-04: Parametric Wiener Filter
    1. How to run the program
        - 請先確認 main.py、WienerFilter.py 與輸入影像 input.tif 位於 Proj05-04 資料夾下
        - 在 Proj05-04 資料夾下執行
            python main.py
        - 程式會先對輸入影像加入 motion blur degradation
        - 接著對 blurred image 加入 Gaussian noise
        - 最後分別使用三種不同的 Wiener filter parameter K 進行影像復原
            K = 0.1
            K = 0.01
            K = 0.001

    2. Output Files
        - out_degraded.tif : 原始影像經過 motion blur degradation 後的結果
        - out_noisy.tif : 在 motion blurred image 上加入 Gaussian noise 後的結果
        - out_K1.tif : 使用 K = 0.1 進行 Wiener filtering 後的 restored image
        - out_K2.tif : 使用 K = 0.01 進行 Wiener filtering 後的 restored image
        - out_K3.tif : 使用 K = 0.001 進行 Wiener filtering 後的 restored image
        - result.png : 將原圖、motion blurred image、blurred noisy image，以及三種 Wiener filtering 結果組合而成的圖片
        - 執行完成後，終端機會顯示不同 K 值對應的 PSNR