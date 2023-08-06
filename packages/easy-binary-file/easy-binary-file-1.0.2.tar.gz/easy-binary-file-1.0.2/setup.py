import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy-binary-file",
    version="1.0.2",
    author="Ramon Invarato Menendez",
    author_email="r.invarato@gmail.com",
    description="Easy way to use binary files with built in class and functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Invarato/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
