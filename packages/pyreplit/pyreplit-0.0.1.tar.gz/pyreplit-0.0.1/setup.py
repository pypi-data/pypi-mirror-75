import setuptools
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(name="pyreplit",
    version="0.0.1",
    description="Fork of sugarfi/pyrepl",
    long_description=read("pyrepl/README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/AgeOfMarcus/pyrepl",
    author="AgeOfMarcus",
    author_email="marcus@marcusweinberger.com",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=read('pyrepl/requirements.txt').split('\n'),
)