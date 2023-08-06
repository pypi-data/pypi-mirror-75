import setuptools

__root__ = 'lib'
__name__ = 'xbrief'
__keywords__ = ["console", "print", "test"]


def including(kw):
    return f"*.{kw}", f"*.{kw}.*", f"{kw}.*", f"{kw}"


with open("README.md", "r") as fh:
    long_description = fh.read()


def read_install_requires():
    return [
        'borel>=0.0.1',
    ]


setuptools.setup(
    name=__name__,
    version="0.0.4",
    author="Hoyeung Wong",
    author_email="hoyeungw@outlook.com",
    description="A console test tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoyeungw/",
    install_requires=read_install_requires(),
    package_dir={'': __root__},
    packages=setuptools.find_packages(where=__root__),  # , include=including(__name__)
    keywords=__keywords__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
