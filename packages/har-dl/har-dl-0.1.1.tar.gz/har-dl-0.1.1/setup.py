from setuptools import setup
from har_dl import __version__


with open("./README.md", "r") as readme:
    long_desc = readme.read()

setup(
    name="har-dl",
    version=__version__,
    author="docyx",
    description="Utility for downloading content from .HAR files",
    packages=["har_dl"],
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/docyx/har-dl",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP"
    ],
    python_requires=">=3.6",
    install_requires=["tqdm"],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "har-dl = har_dl.__main__:main"
        ]
    }
)
