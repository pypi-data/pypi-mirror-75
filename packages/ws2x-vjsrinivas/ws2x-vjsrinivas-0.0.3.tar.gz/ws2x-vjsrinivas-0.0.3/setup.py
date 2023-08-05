import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ws2x-vjsrinivas", # Replace with your own username
    version="0.0.3",
    author="Vijay Rajagopal",
    author_email="vijaythinks@gmail.com",
    download_url = 'https://github.com/vjsrinivas/ws2x-strip/archive/0.0.1.tar.gz',
    description="A simple simulator for WS2812B-style LED strips",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vjsrinivas/ws2x-strip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'opencv-python'
    ],
    python_requires='>=3.0',
)
