import setuptools

__root__ = 'lib'
__keywords__ = ["console", "print", "test"]
__name__ = 'xbrief'


def including(kw):
    return f"*.{kw}", f"*.{kw}.*", f"{kw}.*", f"{kw}"


with open("README.md", "r") as fh:
    long_description = fh.read()


def read_install_requires():
    reqs = [
        'borel>=0.0.1',
    ]
    return reqs


setuptools.setup(
    name=__name__,
    version="0.0.2",
    author="Hoyeung Wong",
    author_email="hoyeungw@outlook.com",
    description="A console test tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoyeungw/",
    install_requires=read_install_requires(),
    package_dir={'': __root__},
    packages=setuptools.find_packages(where=__root__,
                                      include=including(__name__)),
    keywords=__keywords__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
