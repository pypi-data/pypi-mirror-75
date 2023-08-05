import setuptools, os

PACKAGE_NAME = 'xt-models'
VERSION = '0.4.0'
AUTHOR = 'Xtract AI'
EMAIL = 'info@xtract.ai'
DESCRIPTION = 'Models and model utilities for common ML tasks'
GITHUB_URL = 'https://github.com/XtractTech/xt-models'

parent_dir = os.path.dirname(os.path.realpath(__file__))

with open(f'{parent_dir}/README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=GITHUB_URL,
    packages=[
        'xt_models.models',
        'xt_models.models.semantic_segmentation',
        'xt_models.models.object_detection',
        'xt_models.utils'
    ],
    provides=['xt_models'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'torch',
        'torchvision',
        'transformers'
    ],
)
