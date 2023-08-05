import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indOCRArmy",  # Replace with your own username
    version="0.1.8",
    author="Mulya Rahardja Madjiah, Andreas; Hervind; S Fawwazi, Ziyad",
    author_email="ziyad.syauqi95@gmail.com",
    description="A package for reading id and name on KTP and SIM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'numpy', 'opencv-contrib-python', 'pandas',
                     'Pillow', 'torchvision', 'torch==1.5.1', 'matplotlib', 'cudatoolkit==10.2', 'detectron2'],
    python_requires='>=3.8',
)
