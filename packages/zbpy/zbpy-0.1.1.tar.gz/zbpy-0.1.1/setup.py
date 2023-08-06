import setuptools 
from setuptools import setup

modules = ['auth', 'basicqueries', 'queries', 'client', 'cryptography', 'datasci', 'indexedfieldentity', 'pagination', 'permissionentity', 'util', 'zbcert', 'zbprotocol_pb2_grpc', 'zbprotocol_pb2', 'winsign', 'test_zbpy']
dependencies = ['pandas >= 1.0.5',
                'numpy >= 1.19.0',
                'grpcio >= 1.29.0',
                'grpcio-tools >= 1.29.0',
                'phonenumbers >= 8.12.5',
                'ipython >= 6.4.0',
                'ipython-genutils >= 0.2.0',
                'protobuf >= 3.12.2',
                'packaging >= 17.1',
                'starkbank-ecdsa >= 1.0.0 ; platform_system=="Windows"',
                'fastecdsa >= 2.1.2 ; platform_system=="Darwin"',
                'fastecdsa >= 2.1.2 ; platform_system=="Linux"']

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='zbpy',
    version='0.1.1',
    description='A Python SDK for interacting with Zetabase.',
    packages=setuptools.find_packages(),
    #packages=['zbpy'],
    #py_modules=modules,
    #package_dir={'':'zbpy'},
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Database',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zetabase/zbpy',
    author='Austin Hochman',
    author_email='awh76@cornell.edu',
    install_requires=dependencies
)
