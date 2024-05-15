import numpy as np
from PIL import Image

def embed_bit(pixel_value, bit):
    
    cleared_bit = pixel_value & 254
    embedded_value = cleared_bit | bit
    return embedded_value

def Encode(src, message, dest):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n

 
    message += "$$$$$"
    b_message=''
    for i in message:
        b_message = b_message + format(ord(i), "08b")
    req_pixels = len(b_message)
    # print("req_pixels:",req_pixels)
    


    if req_pixels > total_pixels:
        print("Need larger file size")
    else:
        index = 0
        for p in range(total_pixels):
            for q in range(n):
                if index < req_pixels:

                    array[p][q] = embed_bit(array[p][q], int(b_message[index]))
                    index += 1

        
        array = array.reshape(height,width,n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image encoded successfully")

def Decode(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n

    hidden_bits = ""

    for p in range(total_pixels):
        for q in range(0,3): 
           
            hidden_bits += (bin(array[p][q])[-1])

    
    hidden_bytes = [] 
    for i in range(0, len(hidden_bits), 8):
        byte_str = hidden_bits[i:i+8]  

        hidden_bytes.append(byte_str)  

 
    message = ""
    for i in range(len(hidden_bytes)):
        if message[-5:] == "$$$$$":
            break
        else:
            message += chr(int(hidden_bytes[i], 2))
    if "$$$$$" in message:
        print("Hidden message:",message[:-5])
    else:
        print("No hidden message found")



        
def Stego():
    print("Enter the option")
    print("1: Encode")
    print("2: Decode")

    option = input()

    if option == '1':
        print("Enter source image path")
        src = input()
        print("Enter message to hide")
        message = input()
        print("Enter destination image path")
        dest = input()
        print("Encoding...")
        Encode(src,message,dest)

    elif option == '2':
        print("Enter source image path")
        src = input()
        print("Decoding...")
        Decode(src)

    else:
        print("Invalid option")

Stego()

