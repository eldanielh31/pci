from PIL import Image, ImageFilter
import numpy as np


#Funcion encargada de tomar la imagen en formatoBluredImage bmp y aplicarle los filtros de negativo y suavizado y guardarlo
def applyFilter(File_Name):

    Matrix = []

    with open(File_Name, 'r') as file:
        for i in file:
            row = list(map(int, i.split()))
            Matrix.append(row)
    
    Matrix_data = np.array(Matrix, dtype=np.uint8)

    Picture = Image.fromarray(Matrix_data)

    Negative_filter = Image.eval(Picture, lambda x: 255 - x)

    Blur_filter = Picture.filter(ImageFilter.BLUR)

    Picture.save("Image_Original.bmp")
    Negative_filter.save("Image_Negative.bmp")
    Blur_filter.save("Image_Blurred.bmp")

    print("Images processed successfully")


file = "MatImage.txt"

applyFilter(file)