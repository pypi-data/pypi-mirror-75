# coding:UTF-8
# 通过setuptools模块导入所需要的函数
from setuptools import setup, find_packages
setup(
    name="pkgTate",
    version="0.1",
    author="tate",
    url="https://www.github.com/pomelott",
    packages=find_packages("src"),	# src就是模块的保存目录
    package_dir = {"":"src"},   # 告诉setuptools包都在src下
    package_data = {	# 配置其它的文件的打包处理
        # 任何包中含有.txt文件，都包含它 
        "": ["*.txt","*.info","*.properties"],
        # 包含demo包data文件夹中的 *.dat文件
        "": ["data/*.*"],
    },
    exclude=["*.test", "*.test.*", "test.*", "test"] # 取消所有的测试包
)
