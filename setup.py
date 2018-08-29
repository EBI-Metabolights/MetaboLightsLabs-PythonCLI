from setuptools import setup

setup(
	name	=	'uploadToMetaboLightsLabs',	# This is the name of your PyPI-package.
	version	=	'0.2',	# Update the version number for new releases
	install_requires = ['requests'],
	scripts	=	['uploadToMetaboLightsLabs.py']	# The name of your scipt, and also the command you'll be using for calling it
)
