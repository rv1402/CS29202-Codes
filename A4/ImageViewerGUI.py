####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from my_package.data.dataset import Dataset
from my_package.model import InstanceSegmentationModel
from my_package.analysis.visualize import plot_visualization
from my_package.data.transforms import *
from PIL import Image, ImageTk

####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

def setTextEntry(text):
    e.delete(0, tk.END)
    e.insert(0, str(text))

# Define the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor):

    ####### CODE REQUIRED (START) #######
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.

    # Open the file browser dialog
    global img_path
    img_path = tk.filedialog.askopenfilename(initialdir="./", title="Select an image", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    # Load the image
    image = Image.open(img_path)
    width, height = image.size
    # Resize the image
    if width > 600 or height > 600:
        resize = rescale.RescaleImage(600, 'NpArray')
        image = resize(Image.open(img_path))
    else:
        image = np.array(image).transpose((2, 0, 1)) / 255.0
    # Get the predictions from the segmentor
    pred_boxes, pred_masks, pred_class, pred_score = segmentor(image)
    # Call the visualizer to save images with bounding box and masks separately
    plot_visualization(image, pred_boxes, pred_masks, pred_class, pred_score, './', 'output')
    process(clicked.get())

    ####### CODE REQUIRED (END) #######

# `process` function definition starts from here.
# will process the output when clicked.
def process(clicked):

    ####### CODE REQUIRED (START) #######
    # Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
    # Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
    # Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.

    if img_path == None:
        tk.Label(text="Please select an image file first", fg="red", font=("Helvetica", 12)).grid(row=1, column=1)
        return

    # Resize the image to fit window
    resize = rescale.RescaleImage(600, 'PIL')
    # Load the initial image
    initial_img = Image.open(img_path)
    initial_img = resize(initial_img)
    initial_img = ImageTk.PhotoImage(initial_img)
    if clicked == "Segmentation":
        # Show the segmentation
        img = Image.open('./output_mask.png')
    else:
        # Show the bounding boxes
        img = Image.open('./output_bbox.png')
    img = resize(img)
    img = ImageTk.PhotoImage(img)
    # If previous image exists, destroy it
    for widget in picture_frame.winfo_children():
        widget.destroy()
    # Show the image
    label1 = tk.Label(picture_frame, image=initial_img)
    label1.img = initial_img
    label1.grid(row=1, column=0, columnspan=2, sticky='w')
    label2 = tk.Label(picture_frame, image=img)
    label2.img = img
    label2.grid(row=1, column=2, columnspan=2, sticky='e')   
    
    ####### CODE REQUIRED (END) #######

# `main` function definition starts from here.
if __name__ == '__main__':
    img_path = None

    ####### CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    root = tk.Tk()
    root.title("Python GUI | Instance Segmentation | 20CS30045")
    ####### CODE REQUIRED (END) #######

    # Setting up the segmentor model.
    annotation_file = './data/annotations.jsonl'
    transforms = []

    # Instantiate the segmentor model.
    segmentor = InstanceSegmentationModel()
    # Instantiate the dataset.
    dataset = Dataset(annotation_file, transforms=transforms)
    
    # Declare the options.
    options = ["Segmentation", "Bounding-box"]
    clicked = tk.StringVar()
    clicked.set(options[0])

    e = tk.Entry(root, width=70)
    e.grid(row=0, column=0)

    # Create a frame for the picture
    picture_frame = tk.Frame(root)
    picture_frame.grid(row=1, columnspan=4)

    ####### CODE REQUIRED (START) #######
    # Declare the file browsing button
    file_button = tk.Button(root, text="File Browser", command=lambda: [fileClick(clicked, "", segmentor), setTextEntry(img_path)])
    file_button.grid(row=0, column=1)

    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button
    drop = tk.OptionMenu(root, clicked, *options)
    drop.grid(row=0, column=2)

    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    myButton = tk.Button(root, text="Process", command=lambda: process(clicked.get()))
    myButton.grid(row=0, column=3)
    
    ####### CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()
    # Remove the temporary created images
    os.remove('./output_mask.png')
    os.remove('./output_bbox.png')
    ####### CODE REQUIRED (END) #######