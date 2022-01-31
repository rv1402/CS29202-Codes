#Imports
from PIL import Image
import numpy as np
from random import randint


class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''

        # Write your code here
        self.shape = shape
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        if(type(image) is np.ndarray):
            # assuming the image is a (3, H, W) dimensional numpy vector with values lying between 0 and 1
            image = image.transpose((1, 2, 0))
            image = (image * 255).astype(np.uint8)
            image = Image.fromarray(image)

        width, height = image.size
        new_width, new_height = self.shape

        if(self.crop_type == 'center'):
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2
            cropped_image = image.crop((left, top, right, bottom))

        else:
            r = randint(0, (width - new_width))
            c = randint(0, (height - new_height))

            cropped_image = image[r:r+new_height,c:c+new_width]

        cropped_image = np.array(cropped_image).transpose((2, 0, 1)) / 255.0

        return(cropped_image)