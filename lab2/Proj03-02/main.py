import cv2
import HistEqualization as Hist

INPUT_IMAGE = "input.tif"




def main():

    try:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_UNCHANGED)

        output, T = Hist.histEqualization(img)
        
        Hist.drawTransformation(T)

        out_hist = Hist.imageHist(output)
        Hist.drawHistogram(out_hist, "transformed")

        cv2.imwrite("out.tif", output)
        print("Transformed Image is Saved")

        print("All Tasks Done")



    except Exception as e:
        print("Error" + str(e))
        print("Transformation Fails")
        print("Please Try Again")


if __name__ == "__main__":
    main()