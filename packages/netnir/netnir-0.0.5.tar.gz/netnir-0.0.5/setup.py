#!/usr/bin/env python3


import setuptools
from netnir import __version__


setuptools.setup(
    version=__version__,
    name="netnir",
    packages=setuptools.find_packages(),
    install_requires=[
        "pytest-runner",
        "nornir==2.4.0",
        "netmiko==2.4.2",
        "hier_config==v1.6.1",
        "keyring>=21.2.1",
        "keyrings.alt>=3.4.0",
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-black",
        "pytest-flake8",
    ],
    python_requires=">=3.6",
    scripts=["bin/netnir"],
    author="James Williams",
    author_email="james.williams@rackspace.com",
    description="a modular cli utility built around nornir.",
    url="https://github.com/netdevops/netnir",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
)
