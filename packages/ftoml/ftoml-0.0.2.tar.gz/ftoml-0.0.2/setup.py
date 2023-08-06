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

readme_string += subprocess.run(['git', 'tag', '--sort=-v:refname', '-l' , '-n1000', """--format=%(refname:strip=2)
*****

%(contents)"""], stdout=subprocess.PIPE).stdout.decode('utf-8')

version=subprocess.run(['git', 'describe'], stdout=subprocess.PIPE).stdout.decode('utf-8')

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
