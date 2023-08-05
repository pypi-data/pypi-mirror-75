from distutils.core import setup
setup(
        name='testmokuai', # 对外我们模块的名字
        version='1.0',# 版本号
        description='这是第一个对外发布的模块，测试哦',#描述
        author='SmallMing.68gsm',# 作者
        author_email='2295333271@qq.com',
        py_modules=['fabutest.demo1','fabutest.demo2'] # 要发布的模块
)
