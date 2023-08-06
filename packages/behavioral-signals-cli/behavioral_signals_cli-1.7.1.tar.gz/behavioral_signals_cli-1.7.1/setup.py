#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'ruamel.yaml==0.15.94',
    'dotmap==1.3.8', 
    'urllib3>=1.25.8',
    'requests==2.22.0', 
    'python-dateutil==2.8.0',
    'behavioral-signals-swagger-client>=2.7.0', 
    'pyyaml==5.1.2'
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(behavioral-signals): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='behavioral_signals_cli',
    version='1.7.1',
    description="Command Line Interface for Behavioral Signals Emotion and \
    Behavior Recognition Engine in the Cloud",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    author="Behavioral Signals",
    author_email='nassos@behavioralsignals.com',
    url="https://bitbucket.org/behavioralsignals/api-cli/src",
    download_url="https://bitbucket.org/behavioralsignals/api-cli/get/1.7.1.tar.gz",
    packages=find_packages(include=['behavioral_signals_cli']),
    entry_points={
        'console_scripts': [
            'behavioral_signals_cli=behavioral_signals_cli.cmd:main',
            'bsi-cli=behavioral_signals_cli.cmd:main',
            'bsi-meta=behavioral_signals_cli.synth:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='behavioral_signals_cli',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
