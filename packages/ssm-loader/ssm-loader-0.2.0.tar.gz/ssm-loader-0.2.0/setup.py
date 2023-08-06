#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = [
    'awscli==1.18.111',
    'boto3==1.14.34',
    'click==7.1.2'
]

setup(
    name='ssm-loader',
    version='0.2.0',
    py_modules=['ssm'],
    include_package_data=True,
    description='Python app to load SSM',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='DNX Solutions',
    author_email='contact@dnx.solutions',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        ssm=ssm.__main__:main
    ''',
)
