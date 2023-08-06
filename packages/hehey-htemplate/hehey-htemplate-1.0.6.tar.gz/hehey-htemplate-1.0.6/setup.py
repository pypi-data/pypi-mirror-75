# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("./README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

#python3.6 setup.py sdist upload

setup(
    name = 'hehey-htemplate',
    version = '1.0.6',
    author = 'hehe',
    packages=find_packages(),
    author_email = 'chinabluexfw@163.com',
    url = 'https://gitee.com/chinahehe/hehey-htemplate',
    description = 'hehey-htemplate 是一个python 轻量的模板引擎,其主要特点有:易学,示例全,功能全面,html友好标签,编译速度快,易扩展与其他模板引擎对比,其简单易学,速度快(大概1000次编译,800 多毫秒),随时随地编写自己的标签库.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir = {'htemplate': 'htemplate'},
    include_package_data = True
)