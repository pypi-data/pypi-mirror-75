import setuptools

def readme():
    with open("README.md", "r") as fh:
        return fh.read()

setuptools.setup(
    version='0.0.1',
    name="simplemosaic",
    author="Jakub Szkodny",
    author_email="jakubszkodny@gmail.com",
    description="A small example package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/szjakub/simplemosaic",
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)