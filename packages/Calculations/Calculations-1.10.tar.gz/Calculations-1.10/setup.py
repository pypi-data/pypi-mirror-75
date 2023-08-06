from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Calculations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.10',
    packages=find_packages(),
    license='MIT license',
    author_email='cMnethh@gmail.com',
    author='cMneth',
    url="https://github.com/cMneth/calculations",
    description='To calculate equations and draw diagrams',
    install_requires=['matplotlib', 'numpy', 'wheel'],
    classifiers=[
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",

        "Framework :: Matplotlib",
        "Topic :: Scientific/Engineering :: Mathematics",
    ]
)

