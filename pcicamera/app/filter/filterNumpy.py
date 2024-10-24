import numpy as np
from scipy import ndimage
import struct
import os

device_path = "/dev/pci_capture_chr_dev-0"

image_width, image_height = 1920, 1080

def readBytearrayFromTxt(txt_file):
    with open(txt_file, 'rb') as f:
        return bytearray(f.read())

def bmpHeader(width, height):
    file_size = 54 + (width * height * 3)
    
    bmp_header = bytearray(54)
    bmp_header[0:2] = b'BM'
    
    struct.pack_into('<I', bmp_header, 2, file_size)
    struct.pack_into('<I', bmp_header, 10, 54)
    struct.pack_into('<I', bmp_header, 14, 40)
    struct.pack_into('<I', bmp_header, 18, width)
    struct.pack_into('<I', bmp_header, 22, height)
    struct.pack_into('<H', bmp_header, 26, 1)
    struct.pack_into('<H', bmp_header, 28, 24)
    struct.pack_into('<I', bmp_header, 34, width * height * 3)
    
    return bmp_header

def writeBmp(filename, image, width, height):
    with open(filename, 'wb') as f:
        f.write(bmpHeader(width, height))
        f.write(image)

def applyNegativeFilter(image):
    img_array = np.frombuffer(image, dtype=np.uint8).reshape((image_height, image_width, 3))
    negative_image = 255 - img_array
    return negative_image.flatten().tobytes()

def applySmoothingFilter(image, strength=4):
    img_array = np.frombuffer(image, dtype=np.uint8).reshape((image_height, image_width, 3))
    kernel = np.ones((strength * 2 + 1, strength * 2 + 1)) / ((strength * 2 + 1) ** 2)
    smoothed_image = ndimage.convolve(img_array, kernel[:, :, np.newaxis], mode='reflect')
    return smoothed_image.flatten().tobytes()

def invertImageHorizontally(image):
    img_array = np.frombuffer(image, dtype=np.uint8).reshape((image_height, image_width, 3))
    inverted_image = np.flip(img_array, axis=1)
    return inverted_image.flatten().tobytes()

def processImage(image):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    writeBmp(os.path.join(fileDir, "originalImage.bmp"), invertImageHorizontally(image), image_width, image_height)
    
    imgNegative = applyNegativeFilter(image)
    imgSmoothed = applySmoothingFilter(image, strength=4)

    writeBmp(os.path.join(fileDir, "negativeImage.bmp"), invertImageHorizontally(imgNegative), image_width, image_height)
    writeBmp(os.path.join(fileDir, "smoothedImage.bmp"), invertImageHorizontally(imgSmoothed), image_width, image_height)

def writeImageToDevice(image_data):
    try:
        with open(device_path, 'wb') as device_file:
            device_file.write(image_data)
            print("Image written successfully.")
    except Exception as e:
        print(f"Error writing to device: {str(e)}")

def readImageFromDevice():
    try:
        with open(device_path, 'rb') as device_file:
            image_data_from_device = device_file.read(len(image_data))
            print(f"Read {len(image_data_from_device)} bytes from the device.")
            return image_data_from_device
    except Exception as e:
        print(f"Error reading from device: {str(e)}")
        return None

image_data = readBytearrayFromTxt('image_data.txt')[::-1]

writeImageToDevice(image_data)

image = readImageFromDevice()

if image:
    processImage(image)
