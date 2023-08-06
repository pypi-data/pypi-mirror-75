from setuptools import setup                                                # setuptools is our method for building the module
from setuptools import find_packages

from glob import glob

import os

# VERSION
# parse the __planit_version__ variable from python script
VERSION_PATH = os.path.join("src", "planit", "version.py")
exec(compile(open(VERSION_PATH).read(),VERSION_PATH, "exec"))
VERSION = __planit_version__
LICENSE_LOCATION = "https://trafficplanit.github.io/PLANitManual/docs/licenses/"

# RESOURCES
# pars all jars from resource dir
RESOURCE_DIR = "share/planit"
RESOURCE_JAR_FILE_NAMES = glob(RESOURCE_DIR+'/**')                          

setup(
    name="PLANit-Python",
    version= VERSION,
    description="Python API for traffic assignment using PLANit",
    long_description="PLANit-Python enables Python programs running in "
                     "a Python interpreter to configure and run "
                     "a PLANit traffic assignment. It uses Py4J to "
                     "access the underlying Java API that can be used "
                     "for the same purpose",                     
    url="https://trafficplanit.github.io/PLANitManual",
    author="Mark Raadsen",
    author_email="mark.raadsen@sydney.edu.au",                              
    license="modified BSD License (see "+LICENSE_LOCATION+")",              # adopted license
    classifiers=[                                                           # meta information regarding this module
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Java",
        "Topic :: Scientific/Engineering",        
    ],
    packages=["planit", "test_utils"],                                      # we only include these packages  
    package_dir={"": "src"},                                                # indicate the ./src directory is where to find packages rather than this ""
    data_files=[(RESOURCE_DIR, RESOURCE_JAR_FILE_NAMES)],                          # copy all jars in rsc dir as data_files in module
    install_requires=[
          'py4j>='+__py4j_version__,                                        # python installation for py4j
      ],    

)