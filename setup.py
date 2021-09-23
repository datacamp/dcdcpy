#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup details
"""

from setuptools import setup, find_packages


setup(
    author="Richie Cotton [aut, cre], DataCamp [cph, fnd]",
    name='dcdcpy',
    description='DataCamp Data Connector utilities in Python.',
    version='0.0.0.9000',
    packages=find_packages(include=['dcdcpy']),
    install_requires=['boto3', 'awswrangler', 'datetime']
)
