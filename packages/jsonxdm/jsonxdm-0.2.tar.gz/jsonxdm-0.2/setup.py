from setuptools import setup, find_packages

import os
base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()

long_description = """
The *jsonxdm* library provides Python functions to convert JSON data to XML following a simple XML schema called XDM.  
XDM is a low-level intermediate XML-based format that can be used for up-conversion of JSON to other XML formats 
that conform to higher-level XML schemas for specific domains or applications.  It can also be used in the reverse 
direction as intermediate format in down-conversion to JSON.  
"""

setup(
    name="jsonxdm",
    version="0.2",
    packages=find_packages(),
    scripts=['jsonxdm.py'],

    install_requires=['lxml'],

    long_description=long_description,
    author="Pim van der Eijk",
    author_email="pvde@sonnenglanz.net",
    description="Convert between JSON and XML following the XDM schema of XSLT 3.0",
    keywords="xdm, xslt, json, xml, xsd",
    url="https://bitbucket.org/ebcore/jsonxdm/",   # project home page, if any
    project_urls={
        "Documentation": "https://bitbucket.org/ebcore/jsonxdm/",
        "Source Code": "https://bitbucket.org/ebcore/jsonxdm/src/master/",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)
