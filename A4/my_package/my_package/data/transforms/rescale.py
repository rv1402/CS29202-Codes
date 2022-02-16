#Imports
from PIL import Image
import numpy as np

class RescaleImage(object):
    '''
        Rescales the image to a given size.
    '''

    def __init__(self, output_size, type='NpArray'):
        '''
            Arguments:
            output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, larger of image edges is matched
            to output_size keeping aspect ratio the same.
        '''

        # Write your code here
        self.output_size = output_size
        self.type = type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''

        resized_image = None
        # Write your code here
        if(type(image) is np.ndarray):
            # assuming the image is a (3, H, W) dimensional numpy vector with values lying between 0 and 1
            image = image.transpose((1, 2, 0))
            image = (image * 255).astype(np.uint8)
            image = Image.fromarray(image)

        if(type(self.output_size) is tuple):
            resized_image = image.resize(self.output_size)
        else:
            width, height = image.size
            if(width > height):
                width_percent = (self.output_size / float(width))
                height = int(float(height) * float(width_percent))
                resized_image = image.resize((self.output_size, height), Image.NEAREST)
            else:
                height_percent = (self.output_size / float(height))
                width = int(float(width) * float(height_percent))
                resized_image = image.resize((width, self.output_size), Image.NEAREST)

        if(self.type == 'NpArray'):
            resized_image = np.array(resized_image).transpose((2, 0, 1)) / 255.0

        return resized_image