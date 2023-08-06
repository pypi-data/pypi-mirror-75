from os import path as os_path
import setuptools

this_directory = os_path.abspath(os_path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setuptools.setup(
    name="sunyt-mylib-2", # Replace with your own username
    version="0.0.5",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    # install_requires=read_requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)