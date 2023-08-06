import setuptools
from railway import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="railway",  # Replace with your own username
    version=__version__,
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
    install_require=["psycopg2"],
    # extras_require={
    #     "postgres": ["psycopg2", "other_pg_lib"]
    # },
    python_requires='>=3.6',
)
