import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="msr-kouyang",
    version="0.1.1", # Semantic version
    author="Kevin Ouyang",
    author_email="kevinhouyang@gmail.com",
    description="Symops coding challenge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/symopsio/backend-challenge",
    packages=setuptools.find_packages(),
    scripts=['bin/msr'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
