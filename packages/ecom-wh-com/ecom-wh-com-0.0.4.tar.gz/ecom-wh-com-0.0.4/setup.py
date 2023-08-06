#!/usr/bin/env python3


from setuptools import find_packages, setup


setup(
    author="ecomm warehouse Services",
    install_requires=[],
    license="MIT-0",
    name="ecom-wh-com",
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=["pytest"],
    version="0.0.4"
)