#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

install_requires = [
    'rpmvenv',
]

def get_version():
    version = os.environ.get('VERSION', '0.0.0')
    if os.environ.get('RELEASE_TYPE') == "DEV":
        release_parts = os.environ.get('RELEASE').split('.')
        release = "{}.{}{}+{}".format(
            release_parts[0],
            release_parts[1],
            release_parts[2],
            release_parts[3]
        )
        version += "b" + release
    return version


setup_args = dict(
    name='rpmvenv-macros',
    description='Macros extension for rpmvenv',
    long_description='Macros extension for rpmvenv',
    author='Dan Foster',
    author_email='dan@zem.org.uk',
    license="MIT",
    packages=find_packages(),
    platforms=["any"],
    test_suite="tests",
    version='0.0.1',
    install_requires=install_requires,
    entry_points={
        'rpmvenv.extensions': [
            'macros = rpmvenv_macros.macros.macros:Extension',
        ]
    }
)

setup(**setup_args)
