from setuptools import setup

setup(name='pyrman',
	version='0.1',
	description='Python RMAN',
	author='Vladimir Povetkin',
	author_email='vladimir@fido.uz',
	packages=['pyrman'],
	include_package_data=True,
	entry_points="""
    	[console_scripts]
    	pybkp = pyrman.pybkp:main
    	"""
)
