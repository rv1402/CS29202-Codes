#Imports
from my_package.model import InstanceSegmentationModel
from my_package.data.dataset import Dataset
from my_package.analysis.visualize import plot_visualization
from my_package.data.transforms import *
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

def experiment(annotation_file, segmentor, transforms, outputs):
    '''
        Function to perform the desired experiments

        Arguments:
        annotation_file: Path to annotation file
        segmentor: The image segmentor
        transforms: List of transformation classes
        outputs: path of the output folder to store the images
    '''

    #Create the instance of the dataset.
    Data_Set = Dataset(annotation_file, transforms)

    #Iterate over all data items.
    for i in range(len(Data_Set)):
        data, tranformed_images = Data_Set[i]

        #Get the predictions from the segmentor.
        pred_boxes, pred_masks, pred_class, pred_score = segmentor(data['image'])

        #Draw the segmentation maps on the image and save them.
        plot_visualization(data['image'], pred_boxes, pred_masks, pred_class, pred_score, outputs, i)

    #Do the required analysis experiments.
    image = Image.open('./data/imgs/5.jpg')
    np_img_copy = np.array(image).transpose((2, 0, 1))
    np_img = np_img_copy / 255.0

    w, h = np_img.shape[2], np_img.shape[1]
    transformations = [None, flip.FlipImage(), blur.BlurImage(4), rescale.RescaleImage((2*w, 2*h)), rescale.RescaleImage((int(0.5*w), int(0.5*h))), rotate.RotateImage(-90), rotate.RotateImage(45)]

    c=1

    if not os.path.isdir('./transformations/'):
        os.makedirs('./transformations/')

    for transformation in transformations:
        if transformation is None:
            pred_boxes, pred_masks, pred_class, pred_score = segmentor(np_img)

            plot_visualization(np_img, pred_boxes, pred_masks, pred_class, pred_score, './transformations/', c)
        else:                
            pred_boxes, pred_masks, pred_class, pred_score = segmentor(transformation(np_img))

            plot_visualization(transformation(np_img), pred_boxes, pred_masks, pred_class, pred_score, './transformations/', c)

        c = c + 1

def main():
    segmentor = InstanceSegmentationModel()
    experiment('./data/annotations.jsonl', segmentor, [flip.FlipImage(), blur.BlurImage(4)], './output/') # Sample arguments to call experiment()


if __name__ == '__main__':
    main()