#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lxch
#############################################


from setuptools import setup, find_packages

setup(
    name = "requestQ",
    version = "0.0.1",
    keywords = ("pip", "request","requests", "requestQ"),
    description = "就是封装了requests去接口测试",
    long_description = "就是封装了requests去接口测试",
    license = "MIT Licence",

    url = "https://gitee.com/l454124613/request",
    author = "lxch",
    author_email = "lixuechengde@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['paramiko','PyMySQL','requests','sshtunnel']
)