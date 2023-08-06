#!/usr/bin/env python3
from setuptools import setup


setup(
    name='reify',
    version="0.4",
    author="Simon Davy",
    author_email="simon.davy@canonical.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    description="A standalone tool for rendering jinja templates",
    long_description=open('README').read(),
    long_description_content_type='text/plain',
    url="https://github.com/canonical-ols/reify",
    py_modules=['reify'],
    install_requires=[
        'jinja2',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'reify = reify:main',
        ],
    },
)
