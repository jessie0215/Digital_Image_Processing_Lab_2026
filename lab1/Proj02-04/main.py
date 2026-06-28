import cv2
import sys
import interpolation as inter
from fractions import Fraction


input_image = "original.tif"
output_image = "out.tif"

def main():
    
    # prompt the user to input the scaling factor, input file name and output file name
    while True:
        try:
            scale = Fraction(input("Please give a scaling factor (<desired dpi> / <original dpi>, e.g. 100/1250): "))
            if scale <= 0:
                raise ValueError
            else:
                input_image = input("Please specify the file name for input: ") + ".tif"
                output_image = input("Please specify the file name for output: ") + ".tif"
                break  
        except (ValueError,ZeroDivisionError):
            print("Please enter a positive fractional number.")


    try:
        # read the image
        input_raw = cv2.imread(input_image,cv2.IMREAD_UNCHANGED)
        
        # print(input_raw.dtype)
        
        if input_raw is None:
            raise FileNotFoundError("Read Fails")
        
        # call API to get the result
        res = inter.resizeImage_bilinear(input_raw, scale)

        print(input_raw.shape, "->", res.shape)
        
        # write the result to output file
        ok = cv2.imwrite(output_image, res)
        
        if not ok :
            raise Exception("Write Fails")  

    except Exception as e:
        sys.stderr.write("Error:" + str(e) + "\n")

    else:
        print("Conversion Finished")
        print(f"Please Check {output_image}")


if __name__ == "__main__":
    main()