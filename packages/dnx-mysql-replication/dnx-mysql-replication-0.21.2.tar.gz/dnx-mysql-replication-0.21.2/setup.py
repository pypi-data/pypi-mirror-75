#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

import sys

tests_require = []

# add unittest2 to tests_require for python < 2.7
if sys.version_info < (2, 7):
    tests_require.append("unittest2")


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """
        Finds all the tests modules in tests/, and runs them.
        """
        from pymysqlreplication import tests
        import unittest

        unittest.main(tests, argv=sys.argv[:1])


version = "0.21.2"

setup(
    name="dnx-mysql-replication",
    version=version,
    url="https://github.com/DNXLabs/dnx-mysql-replication",
    author="DNX Solutions",
    author_email="contact@dnx.solutions",
    description=("Pure Python Implementation of MySQL replication protocol "
                 "build on top of PyMYSQL."),
    license="Apache 2",
    packages=["pymysqlreplication",
              "pymysqlreplication.constants",
              "pymysqlreplication.tests"],
    cmdclass={"test": TestCommand},
    extras_require={'test': tests_require},
    install_requires=['pymysql'],
)
