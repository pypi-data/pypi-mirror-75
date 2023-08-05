from setuptools import setup, find_packages

setup(
    name="ecws",
    version="3.0",
    keywords=("ecws", "3.0"),

    url="http://test.com",
    author="geiri.sgcc",
    author_email="test@gmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",

    install_requires=[
        "torch==1.5.1",
        "allennlp==1.0.0",
    ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3"
    ]
)
