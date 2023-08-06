# -*- coding: utf-8 -*- 
# @Time : 2019-11-03 14:02 
# @Author : DollarKillerx
# @Description : SetUp
from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="dktools",  # 这里是pip项目发布的名称
    version="0.0.3",  # 版本号，数值大的会优先被pip
    keywords=("pip", "dktools", "featureextraction"),
    description="This is the python tool library written by dollarkiller.",
    long_description="""
    This is the python tool library written by dollarkiller. 
    https://github.com/dollarkillerx/pytools
    """,
    license="MIT Licence",

    url="https://github.com/dollarkillerx/pytools",  # 项目相关文件地址，一般是github
    author="DollarKillerx",
    author_email="dollarkiller@dollarkiller.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    # install_requires = ["numpy"]          #这个项目需要的第三方库
)
