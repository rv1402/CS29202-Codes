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
            image = Image.fromarray(image)
        
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius = self.radius))
        return(blurred_image)