#Imports
from PIL import Image, ImageFilter
import numpy as np

class BlurImage(object):
    '''
        Applies Gaussian Blur on the image.
    '''

    def __init__(self, radius):
        '''
            Arguments:
            radius (int): radius to blur
        '''

        # Write your code here
        self.radius = radius


    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL Image)

            Returns:
            image (numpy array or PIL Image)
        '''

        # Write your code here
        if(type(image) is np.ndarray):
            # assuming the image is a (3, H, W) dimensional numpy vector with values lying between 0 and 1
            image = image.transpose((1, 2, 0))
            image = (image * 255).astype(np.uint8)
            image = Image.fromarray(image)

        blurred_image = image.filter(ImageFilter.GaussianBlur(radius = self.radius))

        blurred_image = np.array(blurred_image).transpose((2, 0, 1)) / 255.0

        return(blurred_image)