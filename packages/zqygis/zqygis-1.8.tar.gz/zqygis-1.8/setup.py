from setuptools import find_packages, setup
setup(
    name='zqygis',
    version='1.8',
    description='zqygis',
    author='zqy',#作者
    author_email='252238741@qq.com',
    url='https://github.com/xxx',
    #packages=find_packages(),
    packages=['zqygis'],  #这里是所有代码所在的文件夹名称
    install_requires=['requests'],
)

