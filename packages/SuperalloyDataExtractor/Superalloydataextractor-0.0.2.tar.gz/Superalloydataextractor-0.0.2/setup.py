# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 09:23:52 2020

@author: 35732
"""

from __future__ import print_function
from setuptools import setup, find_packages
import sys
import setuptools
 
setup(
      name="Superalloydataextractor",
      version="0.0.2",
      author="Weiren_Wang",
      author_email="357329191@qq.com",
      description="A data extractor to get target information from superalloy documents. The functions include batch downloading documents in XML and TXT format from the Elsevier database, locating target sentences from the full text and automatically extracting triple information in the form of <material name, property specifier, value>.",
      long_description=open("README.md",encoding="utf-8").read(),
      keywords='text-mining, mining, superalloy, informatics, nlp, txt, science, scientific',
      license="MIT",
      url="https://github.com/Weiren1996/superalloydataextractor",
      packages=setuptools.find_packages(),
      long_description_content_type="text/markdown",
      classifiers=[
              "Environment :: Web Environment",
              "Intended Audience :: Science/Research",
              "Operating System :: Microsoft :: Windows",
              "Programming Language :: Python :: 3",
              "Topic :: Internet",
              "Topic :: Scientific/Engineering",
              "Topic :: Text Processing",
              ],
      python_requires='>=3.6'
)