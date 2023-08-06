import setuptools


with open('README.md', 'r') as readme:
	long_description = readme.read()


setuptools.setup(

	name='tarvos',
	url=None,
	description='Tarvos Interface Library',
	long_description=long_description,
	long_description_content_type='text/markdown',

	version='0.0.1',
	author='Tanay Gupta',
	author_email='tanayg@protonmail.com',

	packages=setuptools.find_namespace_packages(include=['tarvos.*']),

	install_requires=[
		'pyyaml',
	],

	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],

	python_requires='>=3.6',

)