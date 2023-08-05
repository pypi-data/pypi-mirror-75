"""
setup.py for KVRocket
"""

from setuptools import setup
version = "0.0.0-1" #NOTE: please blame pypi for the weird version numbers...

setup(
    name='kvrocket',
    version=version,
    description="Pure Python Key Value Store",
    url='https://github.com/orcatools/kvrocket',
    author='Dan Sikes',
    author_email='dansikes7@gmail.com',
    keywords='python, key value store',
    packages=[
        'kvrocket'
    ],

    install_requires=[
        'dill'
    ],

    project_urls={
        'Source': 'https://github.com/orcatools/kvrocket',
    },
)