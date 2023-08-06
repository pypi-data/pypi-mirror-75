import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='recordparser',
    version='0.1.0',
    author='Ken Youens-Clark',
    author_email='kyclark@gmail.com',
    description='Parse delimited text files using typed class',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kyclark/python-recordparser',
    packages='.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
