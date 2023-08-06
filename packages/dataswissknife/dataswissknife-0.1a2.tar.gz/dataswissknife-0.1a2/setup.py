import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataswissknife",
    version="0.1a2", # alpha release
    author="Ramshankar Yadhunath",
    author_email="yadramshankar@gmail.com",
    description="A Handy Little Tool to aid your Data Science Projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ry05/dataswissknife",
    packages=setuptools.find_packages(),
    classifiers=[
        # classifiers will help PyPI find the package better
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.7', # version 3.7 is the minimum that is required
    entry_points = {
        # `dsk` is the name of the command line tool to run
        'console_scripts': ['dsk=dataswissknife.cli_tool:main'],
    },
)
