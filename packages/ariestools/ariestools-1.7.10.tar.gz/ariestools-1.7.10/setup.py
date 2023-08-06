#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import setuptools

version = ""
with open('ariestools/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ariestools",
    version=version,
    author="jasonzhang",
    author_email="qwertjkl9090@163.com",
    description="Common Tools for python lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    install_requires=[
        'requests>=2.23.0',
        'urllib3>=1.25.7',
        'PyYAML>=5.3.1',
        'pendulum>=2.1.0',
        'namedtupled>=0.3.3',
        'hues>=0.2.2',
        'tenacity>=6.2.0'
    ],
    packages=setuptools.find_packages(exclude=("test")),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
    exclude_package_data=
    {'':
        [
            "ariestools/graphql_query_util.py",
            "ariestools/json_path_util.py",
            "ariestools/json_util.py",
            "ariestools/path_util.py",
            "ariestools/yaml_util.py",
            "ariestools/object.py",
            "ariestools/arg_util.py",
            "ariestools/time_util.py",
            "ariestools/random_util.py",
            "ariestools/file_util.py",
            "ariestools/color_output.py",
            "ariestools/beauty_print.py"
        ]
    },
)
