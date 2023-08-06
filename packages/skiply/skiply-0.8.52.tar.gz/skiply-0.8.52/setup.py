from setuptools import setup, find_packages

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='skiply',
	version='0.8.52',
	description='Skiply Library',
	author='Caroline Bouchat',
	author_email='caroline@skiply.fr',
    packages=find_packages(),
    namespace_packages=['skiply'],
	zip_safe=False)