# -*- coding: utf-8 -*-
"""
 **********************************************************
 * Author        : tianshl
 * Email         : xiyuan91@126.com
 * Last modified : 2020-07-09 09:46:52
 * Filename      : setup.py
 * Description   : https://packaging.python.org/guides/distributing-packages-using-setuptools/
 * ********************************************************
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xx_wizard',                           # 名称
    version='1.1.1',                            # 版本号
    description='xx精灵: 键盘鼠标的监听与控制',    # 简单描述
    long_description=long_description,          # 详细描述
    classifiers=[
        'License :: OSI Approved :: MIT License',   # 根据MIT许可证开源
        'Programming Language :: Python :: 3',      # 仅与Python3兼容
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',       # 与操作系统无关
    ],
    keywords='keyboard mouse pynput tkinter wizard',  # 关键字
    author='tianshl',                                 # 作者
    author_email='xiyuan91@126.com',                  # 邮箱
    url='https://gitee.com/tianshl/key_wizard',       # 包含包的项目地址
    license='MIT',                                    # 授权方式
    packages=find_packages(),                         # 包列表
    install_requires=['pynput'],
    include_package_data=True,
    zip_safe=True,
)
