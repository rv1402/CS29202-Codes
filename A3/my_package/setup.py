from setuptools import setup, find_packages

setup(
    name='my_package-rv4102',
    version='0.0.1',
    description='Module to perform image segmentation and object detection.',
    license='MIT',
    author='Rushil Venkateswar',
    author_email='rushilv14@gmail.com',
    packages=find_packages(),
    install_requires=['matplotlib','numpy','torch','torchvision','pillow','opencv-python']
)