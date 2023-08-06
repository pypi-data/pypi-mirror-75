from setuptools import setup, find_packages

# See note below for more information about classifiers
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="asyncimg",
    version="1.0.1",
    description="An async image manipulation lib. Can be used for discord.",
    long_description=open("README.md").read() + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shahprog/asyncimg/",
    author="Md Shahriyar Alam",
    author_email="mdshahriyaralam552@gmail.com",
    license="MIT",  # note the American spelling
    classifiers=classifiers,
    keywords="discord discord-rank discord-profile discord-leveling",  # used when people are searching for a module, keywords separated with a space
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "aiohttp",
        "colorthief",
    ],  # a list of other Python modules which this module depends on.  For example RPi.GPIO
    include_package_data=True,
)