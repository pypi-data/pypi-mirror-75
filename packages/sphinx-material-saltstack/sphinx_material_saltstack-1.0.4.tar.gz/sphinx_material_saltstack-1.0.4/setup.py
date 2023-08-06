#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import python libs
import os
import shutil

from setuptools import Command, setup

NAME = "sphinx-material-saltstack"
DESC = "Material sphinx theme for SaltStack documentation"

# Version info -- read without importing
_locals = {}
with open("{}/version.py".format(NAME.replace("-", "_"))) as fp:
    exec(fp.read(), None, _locals)
VERSION = _locals["version"]
SETUP_DIRNAME = os.path.dirname(__file__)
if not SETUP_DIRNAME:
    SETUP_DIRNAME = os.getcwd()

with open("README.md", encoding="utf-8") as f:
    LONG_DESC = f.read()

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()


class Clean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for subdir in (NAME.replace("-", "_"), "tests"):
            for root, dirs, files in os.walk(
                os.path.join(os.path.dirname(__file__), subdir)
            ):
                for dir_ in dirs:
                    if dir_ == "__pycache__":
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    for package in (NAME.replace("-", "_"),):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, ".")
            modules.append(modname)
    return modules


setup(
    name=NAME.replace("-", "_"),
    version=VERSION,
    cmdclass={"clean": Clean},
    description=DESC,
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="Derek Ardolf",
    author_email="derek@icanteven.io",
    url="https://gitlab.com/saltstack/open/docs/sphinx-material-saltstack",
    packages=["sphinx_material_saltstack"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Sphinx :: Extension",
        "Framework :: Sphinx :: Theme",
        "Topic :: Documentation :: Sphinx",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
    ],
    entry_points={
        "sphinx.html_themes": ["sphinx_material_saltstack = sphinx_material_saltstack",]
    },
)
