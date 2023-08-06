import os
from setuptools import find_packages, setup


# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = ["redis"]

testing_extras = [
    "coverage",
]

setup(
    name="redis-simple-mq",
    version="0.3.1",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="Simple message queue based on Redis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ErikKalkoken/",
    author="Erik Kalkoken",
    author_email="kalkoken87@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires="~=3.5",
    install_requires=install_requires,
    extras_require={"testing": testing_extras},
)
