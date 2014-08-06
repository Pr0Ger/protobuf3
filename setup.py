from os import getenv
from setuptools import setup

dependencies = []

try:
    import enum
except ImportError:
    dependencies.append('enum34')

teamcity_build = getenv('TEAMCITY_PROJECT_NAME', False)
version = '0.2'  # Base version
dev = True  # Final or not

if dev:
    if teamcity_build:
        version += 'dev' + getenv('BUILD_NUMBER', '0')
        print(version, file=open('.version', mode='w'))
    else:
        try:
            with open('.version') as f:
                version = f.readline().rstrip()
        except IOError:
            version += 'dev0'  # Unknown revision, so assuming this is the earliest

if teamcity_build:
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
