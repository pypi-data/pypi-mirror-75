import os
import re
from setuptools import setup, find_packages


def get_version():
    """
    Get version from file
    :return:
    """
    version_file = open(os.path.join("datacoco_cloud", "__version__.py"))
    version_contents = version_file.read()
    return re.search('__version__ = "(.*?)"', version_contents).group(1)


setup(
    name="datacoco-cloud",
    packages=find_packages(exclude=["tests*"]),
    version=get_version(),
    license="MIT",
    description="Data common code for AWS Cloud Services by Equinox",
    long_description=open("README.rst").read(),
    author="Equinox Fitness",
    url="https://github.com/equinoxfitness/datacoco-cloud",
    install_requires=[
      'requests==2.*',
      'gevent==1.*',
      'boto3==1.*',
      'future==0.*'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)

