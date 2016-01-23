#!/usr/bin/env python3

from os import getenv
from setuptools import setup

dependencies = []

try:
    import enum
except ImportError:
    dependencies.append('enum34')

teamcity_build = getenv('TEAMCITY_PROJECT_NAME', False)
version = '0.2.1'  # Base version
dev = False  # Final or not
version_ui = version  # Compact version name without build metadata for TeamCity UI

if dev:
    if teamcity_build:
        version += '-dev.{}+{}'.format(getenv('BUILD_NUMBER'), getenv('BUILD_VCS_NUMBER'))
        version_ui += '-dev.{}'.format(getenv('BUILD_NUMBER'))
        print(version, file=open('.version', mode='w'))
    else:
        try:
            with open('.version') as f:
                version = f.readline().rstrip()
        except IOError:
            version += '-alpha'  # Unknown revision, so assuming this is the earliest

if teamcity_build:
    print("##teamcity[buildNumber '" + version_ui + "']")

setup(
    name='protobuf3',
    version=version,
    author='Pr0Ger',
    author_email='me@pr0ger.org',
    url='https://github.com/Pr0Ger/protobuf3',
    license='MIT',
    description='Protocol buffers library for Python 3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=['protobuf3', 'protobuf3.compiler', 'protobuf3.fields'],
    scripts=['bin/protoc-gen-python3'],

    install_requires=dependencies,
)
