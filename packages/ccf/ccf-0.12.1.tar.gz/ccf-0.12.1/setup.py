# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the Apache 2.0 License.

from setuptools import setup  # type: ignore
from os import path

PACKAGE_NAME = "ccf"
UTILITIES_PATH = "utils"

path_here = path.abspath(path.dirname(__file__))

with open(path.join(path_here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=PACKAGE_NAME,
    version="0.12.1",
    description="Set of tools and utilities for the Confidential Consortium Framework (CCF)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/CCF/python/ccf",
    license="Apache License 2.0",
    author="CCF Team",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    packages=[PACKAGE_NAME],
    python_requires=">=3.7",
    install_requires=[
        "msgpack",
        "loguru",
        "requests",
        "requests-http-signature",
        "websocket-client",
        "cryptography",
    ],
    scripts=[
        path.join(PACKAGE_NAME, "proposal_generator.py"),
        path.join(UTILITIES_PATH, "keygenerator.sh"),
        path.join(UTILITIES_PATH, "scurl.sh"),
        path.join(UTILITIES_PATH, "submit_recovery_share.sh"),
    ],
    include_package_data=True,
)
