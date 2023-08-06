#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import ftoml
import subprocess

with open("README.rst") as readme_file:
    readme_string = readme_file.read()

readme_string += """

VERSIONS
########

"""

try: 
    readme_string += subprocess.check_output(['git', 'tag', '--sort=-v:refname', '-l' , '-n1000', """--format=%(refname:strip=2)
*****

%(contents)"""]).decode('utf-8')
except:
    readme_string += "...package build ran in an environment without git?"

try:
    version=subprocess.check_output(['git', 'describe']).decode('utf-8').strip()
except:
    version="0.0.0"



setup(
    name="ftoml",
    version=version,
    description="Python library unifying f-strings"
                "with Tom's Obvious, Minimal Language",
    author="Florian Schüller",
    author_email="florian.schueller@gmail.com",
    url="https://github.com/schuellerf/ftoml",
    packages=['ftoml'],
    license="MIT",
    long_description=readme_string,
    # astroid is a depencency for fstring I needed to install ?!
    install_requires=["toml", "fstring", "astroid"],
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
