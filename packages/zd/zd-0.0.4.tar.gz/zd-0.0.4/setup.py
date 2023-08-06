from setuptools import setup

with open("README.md", 'r') as f:
  long_description = f.read()

with open('requirements.txt') as f:
  install_requires = f.read().splitlines()

setup(
  author="zuroc",
  author_email="zsp042@gmail.com",
  description="file like object for zstandard",
  include_package_data=True,
  install_requires=install_requires,
  name='zd',
  packages=['zd'],
  url="https://gitee.com/znlp/zd",
  version="0.0.4",
  zip_safe=True,
  long_description_content_type='text/markdown',
  long_description=long_description,
  scripts=["zdcat"]
)
