# Imports
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import colorsys
import os
from ..data.transforms.rescale import RescaleImage

def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors

def get_top_3(pred_boxes, pred_masks, pred_class, pred_score):
    """
    Get the top 3 most confident bounding boxes and masks.
    """
    if(len(pred_score) <= 3):
        return pred_boxes, pred_masks, pred_class, pred_score
    else:
        # Find the segmentation masks for only the 3 most confident bounding boxes
        top_3_tuple = sorted(
            zip(pred_score, pred_class, pred_masks, pred_boxes), reverse=True)[:3]

        # # Confidence score filtering is done here
        # top_3_tuple = [i for i in top_3_tuple if i[0] > 0.8]

        # Unpack the tuple
        top_3_score, top_3_class, top_3_masks, top_3_boxes = zip(*top_3_tuple)

        # Return the boxes, masks, class and score
        return top_3_boxes, top_3_masks, top_3_class, top_3_score

def apply_mask(image, mask, color, alpha=0.5):
    """
    Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask != 0, image[:, :, c] *
                                    (1 - alpha) + alpha * color[c] * 255,
                                    image[:, :, c])
    return image

def plot_visualization(image, pred_boxes, pred_masks, pred_class, pred_score, output_path, img_name): # Write the required arguments

    # The function should plot the predicted segmentation maps and the bounding boxes on the images and save them.
    # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.

    # Find the segmentation masks for only the 3 most confident bounding boxes
    boxes, masks, classes, scores = get_top_3(pred_boxes, pred_masks, pred_class, pred_score)

    # Convert image from C, H, W to H, W, C format and scale it
    image = np.copy(image).transpose((1, 2, 0))
    image = (image * 255).astype(np.uint8)

    # Convert masks to H, W, C format and scale them
    masks = [np.squeeze(mask * 255).astype(np.uint8) for mask in masks]

    # Colors to use
    colors = random_colors(len(scores))

    #get width and height of image
    w, h = image.shape[1], image.shape[0]

    # set DPI
    my_dpi = 96

    # If directory does not exist, create it
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    # Create a matplotlib figure, axis
    fig = plt.figure(figsize=(w/my_dpi, h/my_dpi), dpi=my_dpi)
    ax = plt.subplot(111, aspect = 'equal')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    ax.axis('off')
    
    # Draw bounding boxes and save the image
    for i in range(len(boxes)):
        (x1, y1), (x2, y2) = boxes[i]
        # Add the bounding box to the image
        p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, fill=False)
        ax.add_patch(p)
        # Add the label to bounding box
        category = classes[i]
        score = scores[i]
        caption = "{} {:.3f}".format(category, score)
        ax.text(x1, y1 + 12, caption, color='w', size=12, backgroundcolor="none")
    # Save the image
    ax.imshow(image.astype(np.uint8))
    plt.savefig(output_path + str(img_name) + "_bbox.png")

    # Clear previous matplotlib figure
    plt.clf()
    fig = plt.figure(figsize=(w/my_dpi, h/my_dpi), dpi=my_dpi)
    ax = plt.subplot(111, aspect = 'equal')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    ax.axis('off')

    # Create masked_image
    masked_image = np.copy(image)
    # Draw segmentation masks
    for i in range(len(boxes)):
        mask = masks[i]
        color = colors[i]
        # Apply the mask to the image
        masked_image = apply_mask(masked_image, mask, color)
    # Save the image
    ax.imshow(masked_image.astype(np.uint8))
    plt.savefig(output_path + str(img_name) + "_mask.png")