import pathlib

from setuptools import setup, find_packages

from core.constants import PACKAGE_NAME, PACKAGE_ENTRY_POINT

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name=PACKAGE_NAME,
    version_config={
        "version_format": "{tag}.dev{sha}",
        "starting_version": "0.0.1"
    },
    setup_requires=['better-setuptools-git-version'],
    description="Command Line Interface to work with the Seamless Cloud product",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/https://github.com/seamless-io/seamless-cli",
    author="Seamless Cloud",
    author_email="hello@seamlesscloud.io",
    license="ISC",
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=["click~=7.1.2",
                      "requests~=2.23.0",
                      "responses~=0.10.15"],
    entry_points="""
        [console_scripts]
        {entry_point}=core.seamless:cli
    """.format(entry_point=PACKAGE_ENTRY_POINT),
)
