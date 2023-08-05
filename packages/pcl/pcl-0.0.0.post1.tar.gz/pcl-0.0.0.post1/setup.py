"""
setup.py for PCL
"""

from setuptools import setup
version = "0.0.0-1" #NOTE: please blame pypi for the weird version numbers...

setup(
    name='pcl',
    version=version,
    description="PCL is a 'python like' language designed for configuration.",
    url='https://github.com/orcatools/pcl',
    author='Dan Sikes',
    author_email='dansikes7@gmail.com',
    keywords='python, configuration, python configuration language, pcl',
    packages=[
        'pcl'
    ],

    install_requires=[
    ],

    project_urls={
        'Source': 'https://github.com/orcatools/pcl',
    },
)