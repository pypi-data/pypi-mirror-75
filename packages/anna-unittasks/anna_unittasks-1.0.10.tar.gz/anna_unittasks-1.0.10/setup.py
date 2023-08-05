import setuptools

description = "### anna tasks package"

setuptools.setup(
	name='anna_unittasks',
	version='1.0.10',
	author='Patrik Pihlstrom',
	author_email='patrik.pihlstrom@gmail.com',
	url='https://github.com/patrikpihlstrom/anna-unittasks',
	description='anna task package for unittesting',
	long_description=description,
	long_description_content_type='text/markdown',
	install_requires=['anna-lib'],
	packages=['anna_unittasks', 'anna_unittasks.iframe']
)
