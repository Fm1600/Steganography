# Steganography
Steganography using python
Steganography is the practice of hiding a file, message, image or video within another file, message, image or video.
The Python code is to hide text messages using a technique called Least Significant Bit.

Least Significant Bit (LSB) is a technique in which last bit of each pixel is modified and replaced with the data bit. This method only works on Lossless-compression images, which means that the files are stored in a compressed format, but that this compression does not result in the data being lost or modified, PNG, TIFF, and BMP as an example, are lossless-compression image file formats. 
JPG is a lossy compression and thus this code won't support such files.

-----------------  ENCODING --------------------------

Reads the image using PIL.Image.open() function.
Counts the maximum bytes available to encode the data.
Checks whether we can encode all the data into the image.
Finally, modifying the last bit of each pixel and replacing it by the data bit.

------------------------------------------------------

----------------- DECODING  --------------------------

We read the image and then get all the last bits of every pixel of the image. 
We then use bintostring function and check for our stop criteria(used to detect the end of the message to encoded) and decode the message only till the stopping criteria.

------------------------------------------------------

----------------- FILEVALIDATION  ---------------------

checks if the input file is image file or not. Raises error if it's not.

checks the mode of the image file like RGB or RGBA or L and then returns an integer for iteration use in encode/decode functions.


--------------------------------------------------------

------------------  MAIN FUNCTION   ---------------------

Takes user input option for encoding or decoding.
Takes input of data and image source.
Adds the stopping criteria to the rawdata received from user.
Calls respective functions for Encoding/Decoding based on the user selection.



