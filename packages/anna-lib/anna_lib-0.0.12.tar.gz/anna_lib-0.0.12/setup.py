import setuptools

with open('README.md', 'r') as f:
	description = f.read()

setuptools.setup(
	name='anna_lib',
	version='0.0.12',
	author='Patrik Pihlstrom',
	author_email='patrik.pihlstrom@gmail.com',
	url='https://github.com/patrikpihlstrom/anna-lib',
	description='selenium interface',
	long_description=description,
	long_description_content_type='text/markdown',
	packages=['anna_lib', 'anna_lib.task', 'anna_lib.selenium'],
	install_requires=[
		'selenium'
	]
)
