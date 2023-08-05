import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="x_hsky_whl_test", 
    version="0.1.1",
    author="sky",
    author_email="x_hsky@163.com",
    description="A test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
