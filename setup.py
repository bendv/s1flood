from setuptools import setup
import os
import ee

try:
    import eedswe
except ImportError:
    print("The `eedswe` package is optional, but needed to include historical DSWE in flood maps. JRC Global Surface Water data will be used alone in its absence.")
    print("Go to https://github.com/bendv/eedswe for instructions on how to install eedswe")

ee.Initialize()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 's1flood',
    version = '0.0.1',
    packages = ['s1flood',],
    license = 'MIT',
    long_description = read('README.md'),
    long_description_content_type='text/markdown',
    install_requires = [
        'earthengine_api'
        ],
    author = 'Ben DeVries',
    author_email = 'bdv@uoguelph.ca',
    url = 'https://github.com/bendv/s1flood'
)

