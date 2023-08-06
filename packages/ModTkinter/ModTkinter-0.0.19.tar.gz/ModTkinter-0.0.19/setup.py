
import setuptools
#from setuptools import setup, find_packages


with open("README.rst","r") as fh:
    long_description= fh.read()

setuptools.setup(
    name="ModTkinter", # name
    version="0.0.19",
    author="Zin-Lin-Htun",
    author_email="zinlinhtun34@gmail.com",
    description='A Mordernised version of Tkinter, HighDPI for Windows10',
    long_description=long_description,
    #long_description_content_type="text/markdown",
    long_description_content_type="text/x-rst",
    
    keywords="tkinter",
    install_requires=['Pillow'],

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_data={'ModTkinter':['ButDef.png'],'ModTkinter':[]},
    include_package_data = True,
    python_requires='>=3.8',
)


