protobuf3
=========

:Info: Protocol buffers library for Python 3
:Author: Sergey Petrov (Pr0Ger) <me@pr0ger.org>
:Cool badges: |pypi_version| |pypi_downloads| |teamcity_status|

Overview
========

Initial idea of this project was lack of support Python 3 in original `Protocol buffers <https://code.google.com/p/protobuf/>`_
implementation. Currently Google working on this, but currently there is no easy way to use it with
Python 3.

Usage
=====

You should install protobuf compiler. On OS X you can do it with command

.. code-block:: bash
  
  brew install protobuf
    
Install this library with 

.. code-block:: bash
  
  pip install protobuf3

Then you can generate files in similar way like in original protobuf:

.. code-block:: bash

  protoc --python3_out=gen foo.proto
    
Bugs/roadmap
============

I use `YouTrack <http://youtrack.pr0ger.org/issues/PB3>`_ for my projects, so this is a place where
you can find issues related to this project. Unfortunately, free YouTrack instance has accounts limit,
so I can't open registration on it.

Testing
=======

The easiest way to run the tests is to install `nose <https://nose.readthedocs.org/en/latest/>`_
(**easy_install nose**) and run **nosetests** or **python setup.py test** in the root of the distribution.
Tests are located in the *test/* directory.

But good way is using **tox** for launching tests for all supported python versions. If you too lazy
for installing required Python versions you can use `Vagrant <http://vagrantup.com>`_ for bootstraping
test environment by launching **vagrant up** in the root of this distribution. Then login to created
VM by using **vagrant ssh**. Finally, run tests by launching **cd protobuf3 && tox**

.. Images used in readme

.. |pypi_version| image:: http://img.shields.io/pypi/v/protobuf3.svg?style=flat
    :target: https://pypi.python.org/pypi/protobuf3/
    :alt: Version

.. |pypi_downloads| image:: http://img.shields.io/pypi/dm/protobuf3.svg?style=flat
    :target: https://pypi.python.org/pypi/protobuf3/
    :alt: Downloads

.. |teamcity_status| image:: http://img.shields.io/travis/Pr0Ger/protobuf3.svg?style=flat
    :target: https://travis-ci.org/Pr0Ger/protobuf3
    :alt: Build status
