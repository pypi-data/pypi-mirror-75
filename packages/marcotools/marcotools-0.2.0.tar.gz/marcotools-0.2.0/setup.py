import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="marcotools",
    version="0.2.0",
    author="Marco Urriola",
    author_email="marco.urriola@gmail.com",
    description="My Python tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marc0u/marcopytools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
