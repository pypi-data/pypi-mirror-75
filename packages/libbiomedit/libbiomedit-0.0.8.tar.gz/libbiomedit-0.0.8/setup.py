#!/usr/bin/env python3

import os
from datetime import datetime
from setuptools import setup, find_packages

# 0.0.0-dev.* version identifiers for development only (not public)
__version__ = os.environ.get(
    "CI_COMMIT_TAG", "0.0.0.dev" + os.environ.get("CI_JOB_ID", datetime.now().strftime("%Y%m%d")))

setup(
    name="libbiomedit",
    version=__version__,
    license="LGPL3",
    description="Shared library for arround biomedit data transfer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Robin Engler, Jaroslaw Surkont, Riccardo Muri, Gerhard Bräunlich, Christian Ribeaud",
    author_email="Robin.Engler@sib.swiss, "
    "riccardo.murri@id.ethz.ch, "
    "jaroslaw.surkont@unibas.ch, "
    "gerhard.braeunlich@id.ethz.ch, "
    "christian.ribeaud@karakun.com",
    url="https://gitlab.com/biomedit/libbiomedit",
    install_requires=[
        "dataclasses ; python_version<'3.7'",
        "gpg-lite>=0.6.10",
    ],
    packages=find_packages(exclude=["test", "test.*"]),
    python_requires=">=3.6",
    test_suite="test",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
