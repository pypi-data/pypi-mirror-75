import setuptools

description = "### anna tasks package"

setuptools.setup(
	name='anna_tasks',
	version='1.0.13',
	author='Patrik Pihlstrom',
	author_email='patrik.pihlstrom@gmail.com',
	url='https://github.com/patrikpihlstrom/anna-tasks',
	description='anna task package',
	long_description=description,
	long_description_content_type='text/markdown',
	install_requires=['anna-lib'],
	packages=[
		'anna_tasks', 'anna_tasks.base', 'anna_tasks.base.checkout', 'anna_tasks.base.checkout.cart'
	]
)
