from distutils.core import setup
from setuptools import find_packages

setup(
    name='kodex',
    python_requires='>=3',
    version='0.0.1',
    author='KIProtect GmbH',
    author_email='kodex-ce@kiprotect.com',
    license='BSD-3',
    url='https://github.com/kiprotect/kodex-py',
    packages=find_packages(),
    package_data={'': ['*.ini']},
    include_package_data=True,
    install_requires=['click'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            #'beam = beam.cli.main:beam'
        ]
    },
    description='Python bindings for our Kodex tool.',
    long_description=""""""
)
