from distutils.core import setup

setup(
    name='LJmath', #对外我们模块的名字
    version='1.0',   #版本号
    description='这是一个对外发布的模块测试', #描述
    author='LJ',
    author_email='931199510@qq.com',
    py_modules=['LJmath.demo1','LJmath.demo2']    #要发布的模块
)