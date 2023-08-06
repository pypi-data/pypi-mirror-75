import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="setpy", # Replace with your own username
    version="0.0.3",
    author="TJ Ledwith",
    author_email="tjledwith1@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/makertech81/setpy",
    py_modules=["setpy"],
    package_dir={'': 'src'},
#    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "numpy ~= 1.15",
        "matplotlib ~= 3.3.0",
    ],
    python_requires='>=3.6',
)


