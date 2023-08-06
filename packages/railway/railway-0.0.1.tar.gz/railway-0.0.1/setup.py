import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="railway",  # Replace with your own username
    version="0.0.1",
    author="Railway",
    author_email="opensource@railway.app",
    description="Infrastructure, Instantly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/railwayapp/packages/python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
