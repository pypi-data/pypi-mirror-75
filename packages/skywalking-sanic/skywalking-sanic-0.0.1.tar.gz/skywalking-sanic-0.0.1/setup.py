import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skywalking-sanic",
    version="0.0.1",
    author="Parker Zhu",
    author_email="806000178@qq.com",
    description="Skywalking Sanic Support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/parkerzhu/skywalking-sanic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)