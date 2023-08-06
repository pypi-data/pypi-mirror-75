import setuptools

setuptools.setup(
    name="visualcomet",
    version="0.0.7",
    author="Jae Sung Park",
    author_email="jspark96@cs.washington.edu",
    description="Codebase for the Visual COMeT model code",
    dependency_links=[
        # Make sure to install these packages manually!
        "https://download.pytorch.org/whl/cu101/torch-1.5.0%2Bcu101-cp36-cp36m-linux_x86_64.whl",
        "https://download.pytorch.org/whl/cu101/torchvision-0.6.0%2Bcu101-cp36-cp36m-linux_x86_64.whl",
        "https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.5/detectron2-0.2%2Bcu101-cp36-cp36m-linux_x86_64.whl"
    ],
    url="https://github.com/jamespark3922/vcg_demo",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "ftfy==5.1",
        "tqdm",
        "pandas",
        "ipython",
        "opencv-python",
        "pytorch-transformers==1.1.0",
        "allennlp",
    ],
    python_requires='>=3.6',
)