import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageFilter

def resize_for_display(image, size=(500, 300)):
    return image.resize(size, Image.Resampling.LANCZOS)

def open_image():
    filepath = filedialog.askopenfilename(filetypes=[("BMP Files", "*.bmp")])
    if not filepath:
        return

    img_original = Image.open(filepath)
    
    img_negative = apply_negative_filter(img_original)
    img_negative.save("negative_image.bmp")

    img_smoothed = apply_smoothing_filter(img_original)
    img_smoothed.save("smoothed_image.bmp")

    img_original_display = resize_for_display(img_original)
    img_negative_display = resize_for_display(img_negative)
    img_smoothed_display = resize_for_display(img_smoothed)
    
    img_original_tk = ImageTk.PhotoImage(img_original_display)
    label_original.config(image=img_original_tk)
    label_original.image = img_original_tk

    img_negative_tk = ImageTk.PhotoImage(img_negative_display)
    label_negative.config(image=img_negative_tk)
    label_negative.image = img_negative_tk

    img_smoothed_tk = ImageTk.PhotoImage(img_smoothed_display)
    label_smoothing.config(image=img_smoothed_tk)
    label_smoothing.image = img_smoothed_tk

def apply_negative_filter(image):
    return ImageOps.invert(image)

def apply_smoothing_filter(image, radius=3):
    return image.filter(ImageFilter.GaussianBlur(radius))

root = tk.Tk()
root.title("Image Filters Application")
root.geometry("1600x450")

btn_open = tk.Button(root, text="Open Image", command=open_image)
btn_open.grid(row=0, column=1, columnspan=1, pady=10, sticky='ew')

label_original_text = tk.Label(root, text="Original Image")
label_original_text.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

label_negative_text = tk.Label(root, text="Negative Image")
label_negative_text.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

label_smoothing_text = tk.Label(root, text="Smoothed Image")
label_smoothing_text.grid(row=1, column=2, padx=10, pady=10, sticky='ew')

label_original = tk.Label(root)
label_original.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

label_negative = tk.Label(root)
label_negative.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

label_smoothing = tk.Label(root)
label_smoothing.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
