import setuptools
from sys import version

if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None
	
from distutils.core import setup

setuptools.setup(
                    name='mifeco',
                    version='1.0.6',
                    author='@rockscripts',
                    author_email='rockscripts@gmail.com',
                    description='mifeco',
                    long_description="mifeco",
                    install_requires=[],
                    platforms='any',
                    url='https://instagram.com/rockscripts/',
                    packages=['mifeco'],
                    python_requires='>=2.7.*',
                )