from setuptools import setup, find_packages

setup(
    name='robot_neck_fake',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'imutils',
        'numpy',
        'opencv-python'
    ]
)
