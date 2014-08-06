from os import getenv
from setuptools import setup

dependencies = []

try:
    import enum
except ImportError:
    dependencies.append('enum34')

version = '0.2'
dev = True

if dev:
    version += 'dev'

if getenv('TEAMCITY_PROJECT_NAME'):
    if dev:
        version += getenv('BUILD_NUMBER', '')
    print("##teamcity[buildNumber '" + version + "']")

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
