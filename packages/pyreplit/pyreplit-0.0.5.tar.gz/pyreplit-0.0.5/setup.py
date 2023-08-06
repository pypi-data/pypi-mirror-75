import setuptools
import os

setuptools.setup(name="pyreplit",
    version="0.0.5",
    description="Fork of sugarfi/pyrepl",
    long_description=open('README.md','r').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AgeOfMarcus/pyreplit",
    author="AgeOfMarcus",
    author_email="marcus@marcusweinberger.com",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=open('requirements.txt','r').read().split('\n'),
)