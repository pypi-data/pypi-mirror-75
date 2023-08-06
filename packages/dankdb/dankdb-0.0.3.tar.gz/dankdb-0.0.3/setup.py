import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
	name="dankdb",
	version="v0.0.3",
	description="Easy to use database module",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://github.com/DankSideSparkles/DankDB",
	author="Hunter Hopper",
	author_email="hunterlhopper@gmail.com",
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
	],
	packages=["dankdb"],
	include_package_data=True,
	install_requires=[],
	)