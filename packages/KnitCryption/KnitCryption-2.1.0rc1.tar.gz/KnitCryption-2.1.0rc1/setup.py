from setuptools import setup, find_packages

"""
In case you forget the steps to upload your package.

cookiecutter 'some github-url'

1. flake8 #to ensure files are up-to-code... literally
2. pytest #to ensure test cases work properly
3. bumpversion --current-version [version no.] [maj/min] setup.py .\\__init__
4. python setup.py build
5. python setup.py sdist bdist_wheel
6. twine check dist/*
7. twine upload --repository-url https://test.pypi.org/legacy/ dist/*
8. twine upload dist/*
"""

read_README = open('README.txt', mode='r')
README = "".join(read_README.readlines())
read_README.close()

setup(
    name="KnitCryption",
    version="2.1.0.pre1",
    packages=find_packages(),
    scripts=[],
    install_requires=["docutils>=0.3"],
    package_data={
        "": [".txt"]
    },
    author="Keenan W. Wilkinson",
    author_email="keenanwilkinson@outlook.com",
    description="Encrytion package to assist in hiding data",
    long_description=README,
    license="GPL-3.0 license",
    url="https://github.com/WilkinsonK/KnitCryption"
)
