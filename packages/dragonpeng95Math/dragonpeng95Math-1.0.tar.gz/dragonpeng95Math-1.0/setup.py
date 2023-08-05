#coding=utf-8
from distutils.core import setup

setup(
    name="dragonpeng95Math",   #对外我们模块名字
    version = "1.0",           #版本号
    description="这是第一个对外发布的模块，里面只有数学方法，用于测试哦",
    author="dragon",
    author_email="dragonpeng95@163.com",
    py_modules=["dragonpeng95Math.demo1","dragonpeng95Math.demo2"]#要发布的模块
)