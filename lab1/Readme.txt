1. Proj02-02

1.1 Program Description 
This program reduces the number of intensity levels in a grayscale image. The input image is a TIFF file (input.tif), and the program generates a quantized image with reduced intensity levels.

1.2 Requirements
- Python 3.x
- Required libraries:
	- numpy
	- opencv-python (cv2)

1.3 How to Run the Program
- Place the input image "input.tif" in the same directory as the program.
- Run the program using the following command: 
		python main.py
- Enter the desired intensity level when prompted. (Valid values: 2, 4, 8, 16, 32, 64, 128, 256)
- The output image will be saved as: 
	out_<level>.tif    (e.g. out_2.tif) 

1.4 File Structure
- main.py: main program
- util.py: contains reduceIntensityLevel function
- input.tif: input image

2. Proj02-03

2.1 Program Description
This program performs image zooming and shrinking using pixel replication (nearest neighbor interpolation). The program supports both enlargement and reduction of an image according to a user-specified scaling factor.
- If the scaling factor is greater than 1, the image is zoomed. 
- If the scaling factor is less than 1, the image is shrunk.

2.2 Requirements 
Same as Proj02-02

2.3 How to Run the Program
- Place the input image original.tif in the same directory as the program.
- Run the program using the following command:
	python main.py
- Enter the desired scaling factor when prompted.
	Examples:  
		- 10    → zoom in by a factor of 10 
		- 1/10  → shrink by a factor of 10
- Enter the desired input file name and output file name when prompted.
	Examples:
		- original(user input) → original.tif
		- out → out.tif
- The output image will be saved using the file name you specified.
- run the program twice to obtain the two required images
	- original.tif (input) → shrink10.tif (output)
	- shrink10.tif → zoom10.tif

2.4 File Structure
main.py: main program
resize.py: contains resizeImage_replication function
original.tif: given image


3. Proj02-04

3.1 Program Description
This program performs image zooming and shrinking using bilinear interpolation. The program supports both enlargement and reduction of an image according to a user-specified scaling factor.
- If the scaling factor is greater than 1, the image is zoomed. 
- If the scaling factor is less than 1, the image is shrunk.

3.2 Requirements 
Same as Proj02-02

3.3 How to Run the Program
- Place the input image original.tif in the same directory as the program.
- Run the program using the following command:
	python main.py
- Enter the desired scaling factor when prompted.
	Examples:  
		- 100/1250   → shrink by a factor of 0.08 
		- 1250/100  → zoom in by a factor of 12.5
- Enter the desired input file name and output file name when prompted.
	Examples:
		- original → original.tif
		- out → out.tif
- The output image will be saved using the file name you specified.
- Run the program twice to obtain the two required images
	- original.tif (as input) → dpi100.tif (as output)
	- dpi100.tif → dpi1250.tif (this may take a few minutes)

3.4 File Structure
main.py: main program
interpolation.py: contains resizeImage_bilinear function
original.tif: given image