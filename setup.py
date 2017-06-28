import setuptools
from setuptools_behave import behave_test

setuptools.setup(
    setup_requires=['pbr>=2.0.0', 'pytest-runner'],
    tests_require=['pytest', ],
    pbr=True)
