# -*-conding:utf-8-*-
# Base Information:
# @author:      yiyujianghu
# @project:     <sinan>
# @file:        setup.py
# @time:        2020/8/5 4:50 下午

"""
Notes: setup for sinan
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools

setup(
    name='sinan',  # 包的名字
    author='yiyujianghu',  # 作者
    version='0.1.2',  # 版本号
    license='MIT',

    description='A datetime/numberic parser for chinese text',  # 描述
    long_description='''long description''',
    author_email='dongjunyou@126.com',              # 你的邮箱
    url='https://github.com/yiyujianghu',           # 可以写github上的地址，或者其他地址
    # 包内需要引用的文件夹
    packages=setuptools.find_packages(),
    keywords='NLP,NER',
    include_package_data = True,
    platforms = "any",

    # 依赖包
    install_requires=[],
    classifiers=[
        # 'Development Status :: 4 - Beta',
        # 'Operating System :: Microsoft'  # 你的操作系统  OS Independent      Microsoft
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        # 'License :: OSI Approved :: BSD License',  # BSD认证
        'Programming Language :: Python',  # 支持的语言
        'Programming Language :: Python :: 3',  # python版本 。。。
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)
