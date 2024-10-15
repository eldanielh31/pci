from PIL import Image
import numpy as np

image = Image.open('Image.bmp').convert('L')

image_array = np.array(image)


np.savetxt('MatImage.txt', image_array, fmt = '%d')

print("Result has been saved in MatImage.txt")