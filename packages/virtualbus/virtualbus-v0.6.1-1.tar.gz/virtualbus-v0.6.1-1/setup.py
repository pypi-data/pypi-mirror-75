#!/usr/bin/env python3

from distutils.core import setup

from os import path

here = path.abspath(path.dirname(__file__))

#-------------------------------------------------------------------------------

# Package name
name="virtualbus"

# Import version info
exec(open(path.join(here, '{}/version.py'.format(name))).read())

# Long description
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

#-------------------------------------------------------------------------------
# Setup config
setup(
	name = name,
	packages = [name],
	version = __version__,
	license = __license__,
	description = 'Virtual bus',
	long_description = long_description,
	author = __author__,
	author_email = __email__,
	url = f"https://github.com/tedicreations/{name}",
	download_url = "https://github.com/TediCreations/{name}/archive/" + __version__ + '.tar.gz',
	keywords = ['virtual', 'bus', 'socket', 'networking'],
	#install_requires=[],
	entry_points={
	        "console_scripts": [
			"vbus = virtualbus.client:main",
		]
	},
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)
