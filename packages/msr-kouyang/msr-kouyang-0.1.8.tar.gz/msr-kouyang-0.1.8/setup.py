import setuptools

with open("README.md", "r") as fh, open("msr/VERSION", "r") as fv:
    long_description = fh.read()
    version = fv.read()


setuptools.setup(
    name="msr-kouyang",
    version=version,
    author="Kevin Ouyang",
    author_email="kevinhouyang@gmail.com",
    description="Symops coding challenge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/symopsio/backend-challenge",
    packages=setuptools.find_packages(),
    scripts=["bin/msr"],
    include_package_data=True,
    install_requires=[
        "requests",
        "argparse",
        "pkgutil",
        "urllib",
        "multiprocessing",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
