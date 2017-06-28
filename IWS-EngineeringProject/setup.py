from setuptools import setup

setup(
	name="SM_SYS",
	version="0.0.1",
	discription='A web app for requesting features for a selected software',
	license="MIT",
	packages=['SM_SYS'],
	author='Jared Hall',
	author_email='Jared007@live.missouristate.edu',
	include_package_data=True,
	install_requires=['flask', ]
)