from setuptools import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='pdfsearch',
    version='0.0.1',
    packages=['pdfsearch'],
    install_requires=[
        'argparse',
        'pdfminer.six',
        'pathlib',
    ],
    scripts=['pdfsearch/pdfs.py'],
    description='pdf - Search Tool, searches for a keyword in the filename\
            ,the n first pages of the file or in the keyword section of the metadata.',
    long_description = long_description,
    long_description_content_type='text/x-rst',
    author='Holger Wasmund',
    author_email='Holger.Wasmund@gmail.com',
    url='https://gitlab.com/_HolgerW/pdfs.git',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.5.5',
)
