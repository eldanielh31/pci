import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
from filter import processImage

def getPath():
    filepath = filedialog.askopenfilename(filetypes=[("BMP Files", "*.bmp")])
    
    if not filepath:
        return

    return filepath

def applyfilters():
    filepath = getPath()
    
    imgOriginalDisplay, imgNegativeDisplay, imgSmoothedDisplay = processImage(filepath)

    imgOriginalTk = ImageTk.PhotoImage(imgOriginalDisplay)
    imgNegativeTk = ImageTk.PhotoImage(imgNegativeDisplay)
    imgSmoothedTk = ImageTk.PhotoImage(imgSmoothedDisplay)

    labelOriginal.config(image=imgOriginalTk)
    labelOriginal.image = imgOriginalTk

    labelNegative.config(image=imgNegativeTk)
    labelNegative.image = imgNegativeTk

    labelSmoothing.config(image=imgSmoothedTk)
    labelSmoothing.image = imgSmoothedTk


root = tk.Tk()
root.title("Image Filters Application")
root.geometry("1600x450")

btnOpen = tk.Button(root, text="Open Image", command=applyfilters)
btnOpen.grid(row=0, column=1, columnspan=1, pady=10, sticky='ew')

labelOriginalText = tk.Label(root, text="Original Image")
labelOriginalText.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

labelNegativeText = tk.Label(root, text="Negative Image")
labelNegativeText.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

labelSmoothingText = tk.Label(root, text="Smoothed Image")
labelSmoothingText.grid(row=1, column=2, padx=10, pady=10, sticky='ew')

labelOriginal = tk.Label(root)
labelOriginal.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

labelNegative = tk.Label(root)
labelNegative.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

labelSmoothing = tk.Label(root)
labelSmoothing.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
