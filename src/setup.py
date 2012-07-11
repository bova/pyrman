from setuptools import setup
from pyrman.const import APP_VERSION

setup(name='pyrman',
	version=APP_VERSION,
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
