from setuptools import find_packages, setup

setup(
    name='VideoReader',
    packages=find_packages(include=['VideoReader', 'VideoSender']),
    version='0.1.0',
    setup_requires=['pillow', 'opencv-python', 'numpy'],
    description='VideoReader',
    author='VietNhatThai',
    license='MIT',
)