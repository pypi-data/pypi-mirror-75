import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotframework-init",
    version="0.0.5",
    author="YuWeiPeng",
    author_email="404051211@qq.com",
    description="""
    robotframework_init, is a scaffolding which can help you install most robot framework need,
    and it can create a empty project。
    robotframework_init 是一个脚手架工具，通过它可以帮你安装大部分常用的 robot framework需要的包，
    且会生成一个统一文档结构。
    """,
    # py_modules=['robotframework-init'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.cnblogs.com/yicaifeitian/",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent", ]

    ,
    python_requires='>=3.6',
    install_requires=[
        'click>=6.7',
        'selenium>=3.141.0',
        'requests>=2.24.0',
        'robotframework >= 3.1.1',
        'robotframework-seleniumlibrary >= 3.3.1',
        'robotframework-requests >=0.7.0',
        'webdriver-manager >=3.1.0',
        'robotframework-lint >= 1.1.0',
    ]
)