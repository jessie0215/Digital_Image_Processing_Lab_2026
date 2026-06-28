Proj03-01: Image Enhancement Using Intensity Transformations

	To execute the program, run the following command in the terminal:
		python main.py

	The program will prompt the user to enter two parameters:
	1. A constant c, which is used in both the log transformation and the power-law transformation.
	2. A parameter r, which represents the gamma value in the power-law transformation.

	After the program finishes executing, two transformed images will be generated and saved in the current directory:
	1. output_log.tif – the result of the log transformation
	2. output_pow.tif – the result of the power-law transformation

Proj03-02: Histogram Equalization

	To execute the program, run the following command in the terminal:
		python main.py

	During execution, the program will:
	1. Compute the histogram of the original image using the imageHist() function.
	2. Normalize the histogram to obtain the probability distribution.
	3. Compute the transformation function based on the histogram equalization formula.
	4. Apply the transformation function to generate the equalized image.

	After the program finishes executing, the following files will be generated and saved in the current directory:
 	1. original_hist.png – histogram of the original image
	2. transformation.png – the transformation function used for histogram equalization
	3. transformed_hist.png – histogram of the equalized image
	4. out.tif – the histogram equalized image

Proj03-03: Spatial Filtering

	To execute the program, run the following command in the terminal:
		python SpatialFilter.py
	
	During execution, the program will:
	1.Prompt the user to input a mask for spatial filtering and convert the input values into a 2-D mask array.
		In this program, the mask size is fixed at 3×3, so the user needs to input 9 numbers.
		The program will then reshape the input values into a 3×3 mask. For example, if the user enters:
			1 1 1 1 1 1 1 1 1
		the mask will be constructed as:
			1 1 1
			1 1 1
			1 1 1

	2. Read the input image and perform normalization so that all pixel values fall within the range [0,1].
	3. Pad the image with zeros using np.pad() to allow convolution near the image boundaries.
	4. Apply the spatial filtering operation by performing 2-D convolution between the padded image and the user-specified mask using the spatialFiltering() function.
	5. Normalize the filtered image again to ensure the output pixel values remain within the range [0,1].
	
	After the program finishes executing, the following file will be generated and saved in the current directory:
	out_spatialfilter.tif – the spatially filtered image

Proj03-04: Enhancement Using the Laplacian

	To execute the program, run the following command in the terminal:
  		python LaplacianFilter.py

	During execution, the program will:

	1. Prompt the user to input a scale value used in the Laplacian enhancement formula.
	2. Ask the user to specify the mask size for the Laplacian filter. The supported mask sizes are 3×3, 5×5, and 7×7
	3. If the user selects 3×3, the program will further ask whether to include diagonal terms in the Laplacian mask.
    	The user can enter Y or N:

 		Example (without diagonal terms):
  			0 1 0
  			1 -4 1
  			0 1 0

 		Example (including diagonal terms):
  			1 1 1
  			1 -8 1
  			1 1 1

	4. Read the input image and perform normalization so that all pixel values fall within the range [0,1].
	5. Pad the image with zeros using np.pad() to allow convolution near the image boundaries.
	6. Compute the laplacian image by applying spatial filtering using the selected Laplacian mask and the previously implemented spatialFiltering() function.
	7. Multiply the Laplacian result by the user-specified scale value to obtain the scaled Laplacian.
	8. Generate the enhanced image by combining the original image with the scaled Laplacian according to the Laplacian enhancement formula.

	After the program finishes executing, the following files will be generated and saved in the current directory:

	1. out_scaledlaplacian.tif – the Laplacian image (scaled Laplacian response)
	2. out_laplacianfilter.tif – the enhanced image obtained after Laplacian sharpening
