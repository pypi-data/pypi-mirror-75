import setuptools

with open('README.md', 'r') as fh:
	readme = fh.read()

setuptools.setup(
	name='crono-api-client',
	version='0.1.16',
	author='Georges Duverger',
	author_email='georges.duverger@gmail.com',
	description='Crono API client',
	long_description=readme,
	long_description_content_type='text/markdown',
	url='https://github.com/gduverger/crono-api-client',
	license='MIT',
	packages=['crono_api_client'],
	# install_requires=[],
	python_requires='>=3',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers',
		'Natural Language :: English'
	],
)
