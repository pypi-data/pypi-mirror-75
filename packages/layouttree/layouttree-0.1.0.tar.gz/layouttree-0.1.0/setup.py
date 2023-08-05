import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="layouttree",
    version="0.1.0",
    author="pbcquoc",
    author_email="pbcquoc@gmail.com",
    description="Build layout using tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbcquoc/layouttree",
    packages=setuptools.find_packages(),
    install_requires=[
        'anytree==2.8.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
