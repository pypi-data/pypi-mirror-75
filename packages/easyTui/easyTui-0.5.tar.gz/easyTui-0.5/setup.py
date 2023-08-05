import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyTui", # Replace with your own username
    version="0.5",
    author="Ninnjah",
    author_email="yand.man4@gmail.com",
    description="Very simple TUI module for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ninnjah/easyTui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)