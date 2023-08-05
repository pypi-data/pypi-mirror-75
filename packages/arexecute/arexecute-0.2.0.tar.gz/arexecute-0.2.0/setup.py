from setuptools import PackageFinder, setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="arexecute",
    version="0.2.0",
    description="Record and execute actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jurrutiag/arexecute",
    author="Juan Urrutia",
    author_email="juan.urrutia.gandolfo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    packages=find_packages(),
    install_requires=[
        "pynput>=1.6.8",
        "pyautogui>=0.9.50"
    ],
    extras_requires=[
        'twine'
    ],
    entry_points={"console_scripts": ["arexecute=arexecute.__main__:main"]},
)
