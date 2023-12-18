from PIL import Image
import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.withdraw()


def process_images():
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_name = "Processed Images"
    output_dir = os.path.join(desktop_path, folder_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_dir = filedialog.askopenfilenames(title="Select the images to process", filetypes=[("Image Files", "*.jpg"
                                                                                                             ";*.jpeg"
                                                                                                             ";*.png"
                                                                                                             ";*.bmp"
                                                                                                             ";*.jfif"
                                                                                                             ";*.webp")],
                                            multiple=True)

    for input_path in input_dir:
        # Load the image
        image = Image.open(input_path)

        # Invert the colors
        image = image.convert("RGBA")
        r, g, b, a = image.split()
        r = np.array(r)
        g = np.array(g)
        b = np.array(b)
        r = invert_colors(r)
        g = invert_colors(g)
        b = invert_colors(b)
        image = Image.fromarray(np.dstack((r, g, b, a)))

        # Convert to NumPy array
        image = np.array(image)

        # Make the black background transparent
        image[(image[:,:,0] <= 50) & (image[:,:,1] <= 50) & (image[:,:,2] <= 50)] = [0, 0, 0, 0]


        # Save the processed image
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_dir, filename)
        processed_image = Image.fromarray(image)
        processed_image.save(output_path, format='png')

    if len(input_dir) > 0:
        messagebox.showinfo("Success", f"All {len(input_dir)} images have been processed successfully! Images saved "
                                       f"in a "
                                       f"file on desktop")
    else:
        messagebox.showinfo("Error", "No images selected")


def view_output_folder():
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_name = "Processed Images"
    output_dir = os.path.join(desktop_path, folder_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    import subprocess
    subprocess.run(f'explorer "{output_dir}"')


def invert_colors(image):
    return 255 - image


def exit_program():
    main_menu.quit()


main_menu = tk.Tk()
main_menu.title("Main Menu")

main_menu.geometry("300x80")
main_menu.resizable(False, False)

screen_width = main_menu.winfo_screenwidth()
screen_height = main_menu.winfo_screenheight()
x = (screen_width // 2) - (200 // 2)  # 200 is the width of the window
y = (screen_height // 2) - (100 // 2)  # 100 is the height of the window
main_menu.geometry(f"+{x}+{y}")



def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        main_menu.quit()


main_menu.protocol("WM_DELETE_WINDOW", on_closing)

# create the "Process Images" button
process_images_button = tk.Button(main_menu, text="Process Images", command=process_images)
process_images_button.pack()

# create the "View Output Folder" button
view_output_folder_button = tk.Button(main_menu, text="View Output Folder", command=view_output_folder)
view_output_folder_button.pack()

exit_button = tk.Button(main_menu, text="Exit", command=on_closing)
exit_button.pack()

# run the main menu window
main_menu.mainloop()
