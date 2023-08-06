from setuptools import setup
def readme():
	with open('README.md') as f:
		README = f.read()
	return README
setup(
	name="Input-Tools",
	version="1.0",
	description="A Python Package to easily simulate input events",
	long_description=readme(),
	long_description_content_type="text/markdown",
	url="https://github.com/Ahaan123/InputTools",
	license="MIT",
	author="Ahaan Pandya",
	packages=["InputTools"],
	install_requires=["autopy","pynput"],
	include_package_data=True,
	)

