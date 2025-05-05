from setuptools import setup, find_packages

setup(
    name="henpixy",
    version="0.1.15",
    packages=find_packages(),
    install_requires=[
        "pyside6>=6.6.0",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "scikit-image>=0.21.0",
        "matplotlib>=3.7.0"
    ],
) 