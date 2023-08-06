import os
import sys

from setuptools import find_packages, setup

import agiletoolkit as pkg


def read(name):
    filename = os.path.join(os.path.dirname(__file__), name)
    with open(filename) as fp:
        return fp.read()


def requirements(name):
    install_requires = []
    dependency_links = []

    for line in read(name).split("\n"):
        if line.startswith("-e "):
            link = line[3:].strip()
            if link == ".":
                continue
            dependency_links.append(link)
            line = link.split("=")[1]
        line = line.strip()
        if line:
            install_requires.append(line)

    return install_requires, dependency_links


install_requires = requirements("dev/requirements.txt")[0]


if sys.version_info < (3, 7):
    install_requires.append("dataclasses")


meta = dict(
    version=pkg.__version__,
    description=pkg.__doc__,
    name="agile-toolkit",
    author="Luca Sbardella",
    author_email="luca@quantmind.com",
    maintainer_email="luca@quantmind.com",
    url="https://github.com/quantmind/agile-toolkit",
    long_description=read("readme.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={"console_scripts": ["agilekit=agiletoolkit.commands:start"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
)


if __name__ == "__main__":
    setup(**meta)
