#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

with open('AUTHORS.md') as authors_file:
    authors = authors_file.read()

requirements = []

setup(
    name='atos-osiris',
    version="0.0.3",
    author=authors,
    description="Perform generic actions on specific systems",
    long_description=readme + '\n\n' + changelog,
    long_description_content_type='text/markdown',
    url='https://git.atosone.com/osiris/osiris/',
    download='https://git.atosone.com/osiris/osiris/-/archive/master/osiris-master.zip',
    packages=find_packages(),
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Framework :: Flake8',
        'Framework :: Pytest',
        'Framework :: Setuptools Plugin',
        'Framework :: tox',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System'
    ],
    license='Other/Proprietary License',
    entry_points={
        'console_scripts': [
            'osiris=osiris.CLI.OsirisCli:main'
        ]
    },
    install_requires=requirements,
    include_package_data=True,
    keywords=['osiris', 'backup', 'restore', 'openstack'],
    platforms='any',
    zip_safe=True
)
