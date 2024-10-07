import os
from PIL import Image, ImageOps, ImageFilter

def applyNegativeFilter(image):
    return ImageOps.invert(image)

def applySmoothingFilter(image, radius=3):
    return image.filter(ImageFilter.GaussianBlur(radius))

def resizeForDisplay(image, size=(500, 300)):
    return image.resize(size, Image.Resampling.LANCZOS)

def processImage(filepath):
    imgOriginal = Image.open(filepath)

    fileDir = os.path.dirname(os.path.abspath(__file__))

    imgNegative = applyNegativeFilter(imgOriginal)
    imgNegative.save(os.path.join(fileDir, "negativeImage.bmp"))

    imgSmoothed = applySmoothingFilter(imgOriginal)
    imgSmoothed.save(os.path.join(fileDir, "smoothedImage.bmp"))

    imgOriginalDisplay = resizeForDisplay(imgOriginal)
    imgNegativeDisplay = resizeForDisplay(imgNegative)
    imgSmoothedDisplay = resizeForDisplay(imgSmoothed)

    return imgOriginalDisplay, imgNegativeDisplay, imgSmoothedDisplay
