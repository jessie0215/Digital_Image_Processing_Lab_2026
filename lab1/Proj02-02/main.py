import quantization as q
import sys
import cv2

valid_input = [2,4,8,16,32,64,128,256]
INPUT_IMAGE = "input.tif"
output_file =  ""

def main():
    # prompt the user to input the number of intensity level
    while True:
        try:
            level = int(input("Please give a level you want to reduce to: "))
            if level in valid_input:
                output_file = f"out_{level}.tif"
                break
            else:
                print(f"Valid input are: {valid_input}")   
        except ValueError:
            print("Please enter a number.")
        

    try:
        # read the image
        input_raw = cv2.imread(INPUT_IMAGE,cv2.IMREAD_UNCHANGED)
        
        # print(input_raw.dtype)

        if input_raw is None:
            raise FileNotFoundError("Read Fails")
        
        # call the API to get the result
        outcome = q.reduceIntensityLevel(input_raw, level)

        # write the image to output file
        ok = cv2.imwrite(output_file, outcome)
        if not ok :
            raise Exception("Write Fails")  

    except Exception as e:
        sys.stderr.write("Error:" + str(e))
    else:
        print("Conversion Finished")
        print(f"Please Check {output_file}")


if __name__ == "__main__":
    main()



