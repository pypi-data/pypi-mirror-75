
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mneprep", 
    version="0.0.2", 
    author="Katherine Ward",
    author_email="wardk6@cardiff.ac.uk",
    description="Graphical user interface (GUI) for EEG/MEG preprocessing and visualisation with MNE, a Python-based toolbox for neuroimaging data analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "autoreject>=0.2",
        "matplotlib>=3.2,<3.3", 
        "mne>=0.20",
        "numpy>=1.19",
        "PyQt5>=5.10",
        "python-picard>=0.4",
        "QtPy>=1.9",
        "scikit-learn>=0.23",
        "scipy>=1.5"
    ],
    python_requires='>=3.6',
)

