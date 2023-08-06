#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from distutils.cmd import Command
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.sdist import sdist
import shutil

try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.download import PipSession
        from pip.req import parse_requirements


repo_root = os.path.dirname(os.path.abspath(__file__))

class BuildProto(Command):
    description = "Build protobuf file"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pass


class CustomBuildPy(build_py):
    def run(self):
        self.run_command('build_proto')
        build_py.run(self)


class CustomDevelop(develop):
    def run(self):
        self.run_command('build_proto')
        develop.run(self)


class CustomSDist(sdist):
    def run(self):
        self.run_command('build_proto')
        sdist.run(self)

setup(
    name='pygrscope',
    description='',
    long_description='GRAPE: Parallelizing Sequential Graph Computations',
    author='GRAPE Team, Damo Academy',
    author_email='7br@alibaba-inc.com',
    url='https://github.com/dongze/pygrape',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Compilers",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='GRAPE, Graph Computations',

    package_dir={'': '.'},
    packages=find_packages('.'),
    cmdclass={
        'build_proto': BuildProto,
    },
    install_requires=[str(ir.req) for ir in parse_requirements('requirements.txt',
                                                               session=PipSession())
                                  if ir.match_markers()],
)
