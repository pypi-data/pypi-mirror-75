
# from distutils.core import setup
from setuptools import setup


def readme_file():
    with open("README.rst", encoding="utf-8")as rf:
        return rf.read()


setup(name="wdtestlib", version="1.0.1", description="this is a awesome lib2 666 wd", packages=["wdtestlib"], py_modules=["Tool"], author="Sz", author_email="501562071@qq.com", long_description=readme_file(), url="https://github.com/wangshunzi/Python_code", license="MIT")





