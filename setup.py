from setuptools import setup, find_packages

setup(
    name='convertator',
    version='1.0.0',
    packages=find_packages(
        exclude=['tests', 'tests.*', '*.tests', '*.tests.*'],
    ),
    entry_points={
        'console_scripts': [
            'convertator = backend.main:main',
        ],
    },
    requires=[
        'aiohttp (==3.6.2)',
        'cerberus (==1.3.2)',
        'redis (==3.3.11)',
    ],
)