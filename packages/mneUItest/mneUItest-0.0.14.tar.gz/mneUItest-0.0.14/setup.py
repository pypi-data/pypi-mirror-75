
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mneUItest", # Replace with your own username
    version="0.0.14",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    #package_dir={"": "src"},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "autoreject>=0.2",
        "matplotlib>=3.2",
        "mne>=0.20",
        "numpy>=1.19",
        "PyQt5>=5.10",
        "python-picard>=0.4",
        "QtPy>=1.9",
        "scikit-learn>=0.23",
        "scipy>=1.5"
    ],
    #py_modules=[
    #   "bad_chs",
    #    "baseline",
    #    "epochs",
    #    "filter",
    #    "ica",
    #    "load_data",
    #    "notch",
    #    "pipeline_dicts",
    #    "plot",
    #    "plot_func_dialog_classes",
    #    "prep_func_dialog_classes",
    #    "reference",
    #   "resample,"
    #    "save_data"
    #],
    python_requires='>=3.6',
)

