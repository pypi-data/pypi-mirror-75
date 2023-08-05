#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    setup_requires=[
        'pbr', 'setuptools', 'wheel', 'pytest', 'coverage', 'versioneer'
    ],
    pbr=True,
    use_scm_version=True,
)
