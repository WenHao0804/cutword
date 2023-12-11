#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='cutword',
    version='0.0.1',
    python_requires='>=3',
    description='Just Cut Word Faster',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    url='https://github.com/WenHao0804/cutword',
    author='WenHao',
    author_email='wh.wenhao@foxmail.com',
    install_requires=['pyahocorasick'],
    packages=find_packages(),
    package_data={'cutword': ['*.txt']},
    include_package_data=True
)
