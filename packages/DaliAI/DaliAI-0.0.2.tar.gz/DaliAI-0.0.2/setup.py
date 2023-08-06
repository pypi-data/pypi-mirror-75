import setuptools

## 读取本地markdown文件方便我们对我们的库吹牛逼。
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="DaliAI", # 包名
    version="0.0.2", # 版本号
    author="fuhao", # 作者笔名
    author_email="54173723@qq.com", # 作者邮箱
    description="used for AI to change the world!", # 发布包简单介绍
    long_description=long_description, # 将我们吹牛逼的草稿写入包用法中
    long_description_content_type="text/markdown", # 用法的读取格式为markdown格式
    # url="https://github.com/pypa/sampleproject", # 项目地址
    packages=setuptools.find_packages(), # 包需要装哪些python文件，setuptools.find_packages()则为根目录下全部python文件
    include_package_data=True, # MANIFEST.in文件允许导入
    zip_safe=False, # 是否打入压缩包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # 包的最低使用要求
    install_requires= [
        # 'pywin32'
    ], # 此包运行需要哪些其余的第三方库
    project_urls={
        # 'Blog': 'https://blog.csdn.net/qq_45414559/article/details/105560090',
    }, # 介绍包的项目地址
)

