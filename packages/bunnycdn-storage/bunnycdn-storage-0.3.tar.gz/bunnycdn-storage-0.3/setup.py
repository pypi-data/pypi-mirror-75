from setuptools import setup

setup(name='bunnycdn-storage',
    version='0.3',
    description='A python module for the BunnyCDN Storage API',
    url='https://github.com/ajacobsen/bunnycdn-storage',
    author='Andy Jacobsen',
    author_email='atze.danjo@gmail.com',
    license='GPLv3+',
    packages=['bunnycdn_storage'],
    install_requires=['requests'],
    zip_safe=False)