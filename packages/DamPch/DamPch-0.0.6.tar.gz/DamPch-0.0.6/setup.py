import setuptools
#from setuptools import setup, find_packages


with open("README.rst","r") as fh:
    long_description= fh.read()

setuptools.setup(
    name="DamPch", # name
    version="0.0.6",
    author="Zin-Lin-Htun",
    author_email="zinlinhtun34@gmail.com",
    description='A placeholder and string binding models package',
    long_description=long_description,
    #long_description_content_type="text/markdown",
    long_description_content_type="text/x-rst",
    
    keywords="tkinter placeholders",
    install_requires=['hdpitkinter'],

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)


