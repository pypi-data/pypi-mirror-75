import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crsspd",
    version="1.0.8",
    author="Chris Chen",
    author_email="wsywddr@163.com",
    description="This is my personal toolkit.",
    longe_description=long_description,
    longe_description_content_type="text/markdown",
    url="https://github.com/wsywddr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'requests==2.22.0',
        'beautifulsoup4==4.7.1',
        'fake_useragent==0.1.11',
    ]
)