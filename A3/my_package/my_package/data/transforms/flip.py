#Imports
import numpy as np
from PIL import Image


class FlipImage(object):
    '''
        Flips the image.
    '''

    def __init__(self, flip_type='horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''

        # Write your code here
        self.flip_type = flip_type


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

        if(self.flip_type == 'horizontal'):
            flipped_image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
        else:
            flipped_image = image.transpose(method=Image.FLIP_TOP_BOTTOM)

        flipped_image = np.array(flipped_image).transpose((2, 0, 1)) / 255.0

        return flipped_image