import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tsf",
    version="0.1.07",
    description="A library to forecast timeseires data",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Tanushree Halder, Pronojit Saha",
    author_email="tanushree.halder@abzooba.com, pronojit.saha@abzooba.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["tsf"],
    include_package_data=True,
    install_requires=['cython==0.29.14', 'numpy>=1.16',
                      'pandas', 'arch', 'statsmodels', 'pmdarima'],
    entry_points={
        "console_scripts": [
            "timeseries_forecaster=forecaster.__main__:main",
        ]
    },
)
