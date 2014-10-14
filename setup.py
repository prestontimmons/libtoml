from setuptools import setup, find_packages

description = """
A Python toml parser.

https://github.com/prestontimmons/libtoml
"""

setup(
    name="libtoml",
    version="1.0",
    author="Preston Timmons",
    author_email="prestontimmons@gmail.com",
    url="https://github.com/prestontimmons/libtoml",
    description=description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "rply>=0.7.2",
    ]
)
