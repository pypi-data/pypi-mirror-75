import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy_redis_ioc",
    version="0.0.1",
    author="big_bubble",
    author_email="313609467@qq.com",
    description="特定场景下使用的scrapy_redis包，支持redis-cluster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woaidapaopao/scrapy-redis-ioc",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
