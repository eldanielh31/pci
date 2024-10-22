import os
import struct

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
    return bytearray(255 - i for i in image)

def applySmoothingFilter(image, width, height, strength=1, passes=1):
    # Gaussian kernel 3x3
    kernel = [
        1, 2, 1,
        2, 4, 2,
        1, 2, 1
    ]

    kernel = [k * strength for k in kernel]
    kernel_sum = sum(kernel)

    for _ in range(passes):
        new_image = bytearray(len(image))
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                r, g, b = 0, 0, 0
                for ky in range(-1, 2):
                    for kx in range(-1, 2):
                        idx = ((y + ky) * width + (x + kx)) * 3
                        k_val = kernel[(ky + 1) * 3 + (kx + 1)]
                        r += image[idx] * k_val
                        g += image[idx + 1] * k_val
                        b += image[idx + 2] * k_val
                idx_new = (y * width + x) * 3
                new_image[idx_new] = min(255, r // kernel_sum)
                new_image[idx_new + 1] = min(255, g // kernel_sum)
                new_image[idx_new + 2] = min(255, b // kernel_sum)

        image = new_image  

    return new_image

def invertImageHorizontally(image):
    inverted_image = bytearray(len(image))
    for y in range(image_height):
        for x in range(image_width):
            # Calcular el índice del píxel original
            original_index = (y * image_width + x) * 3
            # Calcular el índice del píxel invertido
            inverted_index = (y * image_width + (image_width - x - 1)) * 3
            
            # Copiar los valores RGB
            inverted_image[inverted_index] = image[original_index]
            inverted_image[inverted_index + 1] = image[original_index + 1]
            inverted_image[inverted_index + 2] = image[original_index + 2]

    return inverted_image

def processImage(image):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    writeBmp(os.path.join(fileDir, "originalImage.bmp"), invertImageHorizontally(image), image_width, image_height)
    
    imgNegative = applyNegativeFilter(bytearray(image))
    imgSmoothed = applySmoothingFilter(bytearray(image), image_width, image_height, strength=4, passes=4)

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
