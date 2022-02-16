#Imports
import json
from PIL import Image
import numpy as np

class Dataset(object):
    '''
        A class for the dataset that will return data items as per the given index
    '''

    def __init__(self, annotation_file_path, transforms = None):
        '''
            Arguments:
            annotation_file_path: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''
        annotation_file = open(annotation_file_path)
        self.data = [json.loads(line) for line in annotation_file]
        self.transforms = transforms


    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.data)

    def __getitem__(self, idx):
        '''
            return the dataset element for the index: "idx"
            Arguments:
                idx: index of the data element.

            Returns: A dictionary with:
                image: image (in the form of a numpy array) (shape: (3, H, W))
                gt_png_ann: the segmentation annotation image (in the form of a numpy array) (shape: (1, H, W))
                gt_bboxes: N X 5 array where N is the number of bounding boxes, each
                            consisting of [class, x1, y1, x2, y2]
                            x1 and x2 lie between 0 and width of the image,
                            y1 and y2 lie between 0 and height of the image.

            You need to do the following,
            1. Extract the correct annotation using the idx provided.
            2. Read the image, png segmentation and convert it into a numpy array (wont be necessary
                with some libraries). The shape of the arrays would be (3, H, W) and (1, H, W), respectively.
            3. Scale the values in the arrays to be with [0, 1].
            4. Perform the desired transformations on the image.
            5. Return the dictionary of the transformed image and annotations as specified.
        '''
        img_path = self.data[idx]['img_fn']
        png_ann_path = self.data[idx]['png_ann_fn']
        img = Image.open('./data/' + img_path)
        png_ann = Image.open('./data/' + png_ann_path)

        # perform the transformations
        transformed_images = []
        for transform in self.transforms:
            output = transform(img)
            output = (output.transpose((1, 2, 0)) * 255).astype(np.uint8)
            transformed_images.append(output)

        np_img = np.array(img)
        np_png_ann = np.array(png_ann)

        # convert to numpy array and rescale
        image = np_img.transpose((2, 0, 1))
        gt_png_ann = np_png_ann
        image = image / 255.0
        gt_png_ann = gt_png_ann / 255.0

        bboxes = self.data[idx]['bboxes']
        gt_bboxes = []
        for row in bboxes:
            x1 = row['bbox'][0]
            y1 = row['bbox'][1]
            x2 = row['bbox'][0] + row['bbox'][2]
            y2 = row['bbox'][1] + row['bbox'][3]
            category = row['category']
            bbox = (category, x1, y1, x2, y2)
            gt_bboxes.append(bbox)

        dict = {'image': image, 'gt_png_ann': gt_png_ann, 'gt_bboxes': gt_bboxes}

        return dict, transformed_images