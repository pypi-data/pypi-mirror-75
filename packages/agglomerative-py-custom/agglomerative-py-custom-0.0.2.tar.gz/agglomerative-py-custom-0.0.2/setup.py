import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="agglomerative-py-custom",
    version="0.0.2",
    author="Bervianto Leo Pratama",
    author_email="bervianto.leo@gmail.com",
    description="Agglomerative Custom",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/berv-uni-project/agglomerative-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'pandas',
    ],
    python_requires='>=3.6',
)
