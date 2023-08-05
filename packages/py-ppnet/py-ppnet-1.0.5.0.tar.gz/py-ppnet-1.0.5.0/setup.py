#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup, find_packages
from src.ppnet.config import version

setup(
    name='py-ppnet',
    author='gonewind.he',
    author_email='gonewind.he@gmail.com',
    maintainer='gonewind',
    maintainer_email='gonewind.he@gmail.com',
    url='https://gitee.com/gonewind73/pytuntap',
    description='P2P network',
    long_description=open('README.rst',"rt",encoding="utf8").read(),
    long_description_content_type = 'text/x-rst',
    version= version,
    install_requires=[     ], #windows
    python_requires='>=3',
    platforms=["Linux","Windows"],
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: System :: Networking'],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={'console_scripts': [
          'ppnet_chat = ppnet.ppchat:main'],
          'gui_scripts': [
              ]}
      )
