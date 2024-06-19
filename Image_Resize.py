import os
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, messagebox
from PIL import Image

def compress_image(input_path, output_path, target_size_kb, step=10, quality=85):
    """
    Compress an image to a target file size.

    :param input_path: Path to the input image.
    :param output_path: Path to save the output image.
    :param target_size_kb: Desired file size in kilobytes.
    :param step: The decrement in quality for each iteration.
    :param quality: Initial quality setting for compression.
    """
    # Open the image
    img = Image.open(input_path)
    
    # Calculate initial file size
    img.save(output_path, quality=quality)
    file_size_kb = os.path.getsize(output_path) / 1024
    
    # Adjust quality until the target size is met
    while file_size_kb > target_size_kb and quality > step:
        quality -= step
        img.save(output_path, quality=quality)
        file_size_kb = os.path.getsize(output_path) / 1024
    
    return file_size_kb, quality

def browse_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    input_path_var.set(file_path)

def compress_image_gui():
    input_path = input_path_var.get()
    output_path = output_path_var.get()
    try:
        target_size_kb = int(target_size_var.get())
        if not input_path or not output_path:
            raise ValueError("Input or output path is missing.")
        
        final_size_kb, final_quality = compress_image(input_path, output_path, target_size_kb)
        messagebox.showinfo("Success", f"Image compressed to {final_size_kb:.2f} KB with quality={final_quality}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = Tk()
root.title("Image Compressor")

# Create and set variables
input_path_var = StringVar()
output_path_var = StringVar()
target_size_var = StringVar()

# Create and place widgets
Label(root, text="Select Image:").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=input_path_var, width=50).grid(row=0, column=1, padx=10, pady=5)
Button(root, text="Browse", command=browse_image).grid(row=0, column=2, padx=10, pady=5)

Label(root, text="Save As:").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=output_path_var, width=50).grid(row=1, column=1, padx=10, pady=5)
Button(root, text="Browse", command=lambda: output_path_var.set(filedialog.asksaveasfilename(defaultextension=".jpg"))).grid(row=1, column=2, padx=10, pady=5)

Label(root, text="Target Size (KB):").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=target_size_var, width=50).grid(row=2, column=1, padx=10, pady=5)

Button(root, text="Compress", command=compress_image_gui).grid(row=3, column=0, columnspan=3, padx=10, pady=20)

# Start the main event loop
root.mainloop()
