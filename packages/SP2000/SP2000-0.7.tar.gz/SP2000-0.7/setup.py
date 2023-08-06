import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SP2000",
    version="0.7",
    author="Hao Li",
    author_email="lihao@mail.ynu.edu.cn",
    description="sp2000 python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ynulihao/SP2000",
    packages=setuptools.find_packages(),
    install_requires=['pandas','requests'],
    entry_points={
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)