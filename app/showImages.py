import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

def resizeImage(file_path, width, height):
    image = Image.open(file_path)
    image = image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(image)

def showImages():
    window_width = 1920
    window_height = 1080

    img_width = window_width - 250
    img_height = window_height - 150

    root = tk.Tk()
    root.title("Visualizador de Imágenes")
    root.geometry(f"{window_width}x{window_height}")

    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((window_width // 2, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame.columnconfigure(0, weight=1)

    original_image_path = os.path.join(os.path.dirname(__file__), "output/simics/originalImage.bmp")
    negative_image_path = os.path.join(os.path.dirname(__file__), "output/simics/negativeImage.bmp")
    smoothed_image_path = os.path.join(os.path.dirname(__file__), "output/simics/smoothedImage.bmp")

    original_img = resizeImage(original_image_path, img_width, img_height)
    negative_img = resizeImage(negative_image_path, img_width, img_height)
    smoothed_img = resizeImage(smoothed_image_path, img_width, img_height)

    for i, (title, img) in enumerate([
        ("Imagen Original", original_img),
        ("Imagen Negativa", negative_img),
        ("Imagen Suavizada", smoothed_img)
    ]):
        
        image_frame = ttk.Frame(scrollable_frame)
        image_frame.grid(row=i*2, column=0, pady=20, padx=20)

        title_label = tk.Label(image_frame, text=title, font=("Arial", 16))
        title_label.pack()

        image_label = tk.Label(image_frame, image=img)
        image_label.pack()


    def on_mouse_wheel(event):
        if event.delta:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        else: 
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

    root.bind_all("<MouseWheel>", on_mouse_wheel)  
    root.bind_all("<Button-4>", on_mouse_wheel)    
    root.bind_all("<Button-5>", on_mouse_wheel)    
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

if __name__ == "__main__":
    showImages()
