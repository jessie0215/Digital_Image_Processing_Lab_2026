Proj04-01: Two-Dimensional Fast Fourier Transform
    1. How to run the program
        - 請先確認 main.py、DFT.py 與輸入影像 input.tif 位於 Proj04-01 資料夾下
        - 以及 Gaussian Lowpass Filter 的實作檔案位於 Proj04-03 資料夾下
        - 在 Proj04-01 資料夾下執行
            python main.py
        - 執行後，程式會詢問是否需要 zero padding： Please specifiy if zero padding is needed (Y/N):
            Y 或 y：表示啟用 zero padding
            N 或 n：表示不使用 zero padding
    2. Program Description
        - 讀入 input.tif
        - 將影像轉成 float32 並縮放成 256 x 256
        - 視使用者輸入決定是否進行 zero padding
        - 將影像乘上 (-1)^(x+y)，把頻譜中心移到影像中央
        - 使用自行實作的 myDFT2() 計算 2-D DFT
        - 產生 Gaussian Lowpass Filter
        - 在 frequency domain 中將頻譜與 filter 相乘
        - 使用自行實作的 myIDFT2() 做反轉換
        - 再乘一次 (-1)^(x+y)，把影像移回原本位置
        - 若有做 zero padding，最後再 crop 回 256 x 256
        - 將各階段結果輸出成影像檔，方便觀察
        - 將結果彙整並利用 pyplot 畫出包含輸入和所有輸出影像的圖
    3. Output Files
        如果沒有做 zero padding : 
        - shifted_img.tif : 將原始影像乘上 (-1)^(x+y) 後的結果。
        - spectrum.tif : 原影像經 DFT 後的頻譜圖。
        - filter.tif : Gaussian Lowpass Filter。
        - filtered_spectrum.tif : 原始頻譜與 Gaussian Lowpass Filter 相乘後的頻譜圖。
        - output.tif : 最終輸出的 filtered image。
        如果有做 zero padding，程式將輸出以下檔案 : 
        - zero_pad.tif : 原始影像做 zero padding 後的結果。
        - shifted_img.tif : zero padded image 乘上 (-1)^(x+y) 後的結果。作用與未 padding 情況相同，是將低頻移到中心。
        - spectrum.tif : padded image 做 DFT 後的頻譜圖。
        - filter.tif : 與 padded image 同尺寸的 Gaussian Lowpass Filter。
        - filtered_spectrum.tif : 頻譜與 Gaussian Lowpass Filter 相乘後的結果。
        - filtered_raw.tif : IDFT 後、但尚未 crop 的完整結果。
        - output_zero_pad.tif : 最終裁切回 256 x 256 的 filtered image。
        - result.png : 將 input.tif 以及上述 7 張圖組合而成的圖片

Proj04-02: Fourier Spectrum and Average Value
    1. How to run the program
        - 請先確認 main.py 與輸入影像 Fig0441(a).tif 位於 Proj04-02 資料夾下
        - 在 Proj04-02 資料夾下執行
            python main.py
    2. Program Description
        - 讀入 input.tif
        - 將影像轉成 float32 型態
        - 建立 (-1)^(x+y) mask，並將影像乘上此 mask，此步驟用來將頻譜中心移至影像中央（centered spectrum）
        - 使用 numpy.fft.fft2() 計算 2-D Fourier Transform
        - 計算頻譜 magnitude，並使用 log(1 + |F(u,v)|) 增強顯示效果
        - 將頻譜輸出為影像檔案
        - 直接對原始影像計算平均值（mean_direct）
        - 從 centered Fourier spectrum 的中心點 (M/2, N/2) 取得 DC 成分並除以 (M × N) 得到 mean_from_spectrum
        - 輸出兩種方法計算得到的平均值以供比較
        - 將結果彙整並利用 pyplot 畫出包含輸入和輸出影像的圖
    3. Output
        - spectrum.tif : 原始影像經過 centered Fourier Transform 後的頻譜圖
        - 執行完成後，終端機會顯示直接計算的 mean 和 由 Fourier spectrum 計算的 mean 
        - result.png : 將 input.tif 以及 spectrum.tif 組合而成的圖片

Proj04-03: Lowpass Filtering
    1. How to run the program
        - 請先確認 main.py、LowPass.py 與輸入影像 input.tif 位於 Proj04-03 資料夾下
        - 在 Proj04-03 資料夾下執行
            python main.py
        - 程式會依序使用數個 cutoff frequency（D0）進行 Gaussian Lowpass Filtering (specify in D0_list)
        - 每個 D0 都會輸出一張對應的 filtered image
    2. Program Description
        - 讀入 input.tif，並轉為 float32 型態
        - 將影像做 zero padding，尺寸擴展為 2M × 2N
        - 建立 (-1)^(x+y) mask，將影像乘上此 mask，使頻譜中心移至影像中央（centered spectrum）
        - 使用 numpy.fft.fft2() 計算 2-D Fourier Transform
        - 使用 myGLPF(D0, M, N) 產生 Gaussian Lowpass Filter
        - 在 frequency domain 中將頻譜與 Gaussian Lowpass Filter 相乘
        - 使用 numpy.fft.ifft2() 做反傅立葉轉換（IDFT）
        - 再乘一次 (-1)^(x+y)，將影像移回原本位置
        - 將結果 crop 回原始影像大小 M × N
        - 對不同 D0 重複上述流程，以觀察 lowpass filtering 的效果變化
        - 將結果彙整並利用 pyplot 畫出包含輸入和所有輸出影像的圖
    3. Output Files
        使用不同的 D0 進行 Lowpass Filtering 所產生的結果圖 : 
        - out_10.tif
        - out_30.tif
        - out_60.tif
        - out_160.tif
        - out_460.tif 
        - result.png : 將 input.tif 以及上述 5 張圖組合而成的圖片

Proj04-04: Highpass Filtering
    1. How to run the program
        - 請先確認 main.py、HighPass.py 與輸入影像 input.tif 位於 Proj04-04 資料夾下
        - 在 Proj04-04 資料夾下執行
            python main.py
        - 程式會依序使用不同 cutoff frequency（D0）進行 Gaussian Highpass Filtering (specify in D0_list)
        - 每個 D0 都會輸出一張對應的 highpass image
    2. Program Description
        - 讀入 input.tif，並轉為 float32 型態
        - 將影像做 zero padding，尺寸擴展為 2M × 2N
        - 建立 (-1)^(x+y) mask，將影像乘上此 mask，使頻譜中心移至影像中央（centered spectrum）
        - 使用 numpy.fft.fft2() 計算 2-D Fourier Transform
        - 使用 myGHPF(D0, M, N) 產生 Gaussian Highpass Filter（H = 1 - GLPF）
        - 在 frequency domain 中將頻譜與 Gaussian Highpass Filter 相乘
        - 使用 numpy.fft.ifft2() 做反傅立葉轉換（IDFT）
        - 再乘一次 (-1)^(x+y)，將影像移回原本位置
        - 將結果 crop 回原始影像大小 M × N
        - 輸出一張對應的 highpass image
        - 對不同 D0 重複上述流程，以觀察 highpass filtering 的效果變化
        - 將結果彙整並利用 pyplot 畫出包含所有輸出影像的圖
    3. Output Files
        使用不同的 D0 進行 Highpass Filtering 所產生的結果圖 : 
        - out_60.tif
        - out_160.tif 
        - result.png : 將上述 2 張圖組合而成的圖片