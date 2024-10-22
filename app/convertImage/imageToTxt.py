from PIL import Image
import os

def saveBytearrayToTxt(image_name, output_txt):
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_name)
    img = Image.open(image_path)
    img = img.convert('RGB')

    image_data = bytearray(img.tobytes())

    with open(output_txt, 'wb') as f:
        f.write(image_data)

def readBytearrayFromTxt(file_name):
    with open(file_name, 'rb') as f:
        return bytearray(f.read())

def createImageFromBytearray(image_data, width, height, output_image_name):
    img = Image.frombytes('RGB', (width, height), bytes(image_data))
    img.save(output_image_name)


saveBytearrayToTxt('image.bmp', 'image_data.txt')

image_data = readBytearrayFromTxt('image_data.txt')
original_image = Image.open('image.bmp')
width, height = original_image.size

createImageFromBytearray(image_data, width, height, 'new_image.bmp')
