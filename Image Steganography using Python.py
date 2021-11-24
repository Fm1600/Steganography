from typing import Text
import cv2
import numpy as np
from PIL import Image
from PIL import UnidentifiedImageError

################################Logic for Binary to String conversion.#################
def BinarytoString(bin_data):
# initializing a empty string for storing the string data
    str_data =' '
  
# slicing the input and converting it in decimal and then converting it in string
    for i in range(0, len(bin_data), 8):
    # slicing the bin_data from index range [0, 6]
    # and storing it in temp_data
        temp_data = bin_data[i:i + 8]
    # passing temp_data in BinarytoDecimal() function
    # to get decimal value of corresponding temp_data
        decimal_data = int(temp_data,2)
      
    # Decoding the decimal value returned by int function,  using chr()
    # function which return the string corresponding character for given ASCII value, and store it
    # in str_data
        str_data = str_data + chr(decimal_data)
        if(str_data[-4:]=='===='):
            break
    if(str_data.find('====')== -1):
        print('End string not found, either the image is not encoded with any data or different steg tool was used for encoding!!')
        exit()
    else:
        return(str_data[:-4])
##############################  End of Binary to ascii Method   ##########################

##############################  CONVERT TEXT INPUT TO BINARY    ############################
def TexttoBin(test_str): 
    # using join() + bytearray() + format()
    # Converting String to binary
    res = ''.join(format(i, '08b') for i in bytearray(test_str, encoding ='utf-8'))
    return str(res)
########################    END OF THE TEXT TO BINARY   ###############################


##########################      ENCODING LOGIC      ############################################
def encoding(image_name,data,m):
    i=0
    with Image.open(image_name) as img:
        
        
        n_bytes = img.size[0]*img.size[1] * m // 8
        print("Max possible bytes is: ",n_bytes)
        if(len(data)>n_bytes):
            raise ValueError("[!] Insufficient bytes available, need bigger image or less data.")
            exit()
        print('--------------Encoding the Image---------------------')
        #give width and height of the image
        width, height = img.size
        print("width is", width,'\nHeight is: ', height)
        #piccel=list(img.getpixel((0,0)))
        #iterate through each and every pixel through entire image 
        for x in range(0, width):
            for y in range(0, height):
                #get pixels of the image as a list like [R, G, B, A]
                pixel = list(img.getpixel((x, y)))
                #iterate thorugh rgba of the current pixel
                for n in range(0,m):
                    if(i < len(data)):
                        #it take a value from pixel list eg. (0,10,2,255) so it takes
                        #10 since pixel[1] is 10 and then 10 ands with 0 means the LSB of for all such RGB in pixcels becomes zero
                        #then we or it with our data bits..
                        # so that whatever bit are there in our data, it goes into the lsb of the pixel's R, G, B
                        pixel[n] = pixel[n] & ~1 | int(data[i])
                        i+=1
                #replaces the pixel in image with edited pixel in variable pixel
                # and since its a tuple we need to make it a tuple
                img.putpixel((x,y), tuple(pixel))
        #saving it as new image        
        img.save("source_secret.png", "PNG")
        print("Done: Image is encoded with the text Successfully")
 #########################   END OF ENCODING LOGIC   ########################################

##########################      DECODING LOGIC      #########################################   
def decoding(image_name,m):
    extracted_bin = []
    
    with Image.open(image_name) as img:
        print("--------------------Decoding the Image--------------------")
        width, height = img.size
        ext=list(img.getpixel((0,0)))[0]    
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(img.getpixel((x, y)))
                
                for n in range(0,m):
                    pixbin=str(bin(pixel[n]&1))
                    extracted_bin.append(pixbin[-1])

    data = "".join([str(x) for x in extracted_bin])
    decoded_data=BinarytoString(data)
    return decoded_data

########################  END OF DECODING LOGIC    ####################################

###################### black and white encode logic #############
def encodingblackandwhite(image_name,data,m):
    i=0
    with Image.open(image_name) as img:
        n_bytes = img.size[0]*img.size[1] * m // 8
        print("Max possible bytes is: ",n_bytes)
        if(len(data)>n_bytes):
            raise ValueError("[!] Insufficient bytes available, need bigger image or less data.")
        print('--------------Encoding the Image---------------------')
        #give width and height of the image
        width, height = img.size
        print("width is", width,'\nHeight is: ', height)
        for x in range(0, width):
            for y in range(0, height):
                pixel = (img.getpixel((x, y)))
                if i<len(data):
                    pixel = pixel & ~1 | int(data[i])
                    i+=1
                img.putpixel((x,y),pixel)
        #saving it as new image        
        img.save("source_secretbw.png", "PNG")
        print("Done: BW Image is encoded with the text Successfully")
################################################################

######################## Decode Black and White Image ########################
def decodingblackandwhite(image_name):
    extracted_bin = []
    with Image.open(image_name) as img:
        print("--------------------Decoding the Image--------------------")
        width, height = img.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = img.getpixel((x, y))
                pixbin=str(bin(pixel&1))
                extracted_bin.append(pixbin[-1])
    data = "".join([str(x) for x in extracted_bin])
    decoded_data=BinarytoString(data)
    return decoded_data
##############################################################################


######################### VALIDATION FUNCTION ##################################
def Filevalidation(input_image):
    try:
        with Image.open(input_image) as img:
            if img.format not in ('BMP','PNG','TIFF'):
                print('Only Lossless compresssion Images are supported, Please select BMP or PNG extension Images')
                return [False,0]
            if(img.mode=='L'):
                m=1
            elif(img.mode=='RGB'):
                m=3
            elif(img.mode=='RGBA'):
                m=4
            print("The mode is", m)
            return [True,m]
    except UnidentifiedImageError:
        print("Only Image type Files are supported, Please Select an Image File")
        return [False,0]
    except FileNotFoundError:
        print("The File location seems invalid, Please Enter correct File Location")
        return [False,0]
########################   MAIN DRIVER FUNCTION    #########################################

if __name__ == "__main__":
   while True:
            
        print('------------------ IMAGE STEGANOGRAPHY-------------------')
        a = int(input("Welcome to Image Steganography \n Select one of the below options \n"
                            "1. Encode\n2. Decode\n3. Exit\n" ))
        if (a == 1):
            input_image =input("Enter the Image Location: ")
            rawdata=input('Enter some text to encode into the image: ')
            #"011011000110010101100100011001110110010101110010" #ledger
            rawdata+="===="
            data=TexttoBin(rawdata)
            IsValid=Filevalidation(input_image)
            if(IsValid[0]== False):
                continue
            # encode the data into the image
            mode=IsValid[1]
            if(mode==1):
                encoded_image=encodingblackandwhite(input_image,data,mode)
                break
            else:
                encoded_image = encoding(image_name=input_image,data=data,m=mode)
                break
    
        elif (a == 2):
            # decode the secret data from the image
            input_image=input("Enter the Image Location: ")
            IsValid=Filevalidation(input_image)
            if(IsValid[0]== False):
                continue
            mode=IsValid[1]
            if(mode==1):
                decoded_data=decodingblackandwhite(input_image)
            else:
                decoded_data = decoding(input_image,mode)
            print("The decoded data is ",decoded_data)
            print("-----------------------------------")
            break
        elif(a==3):
            break
        else:
            print("Enter correct input")
    
    
    




