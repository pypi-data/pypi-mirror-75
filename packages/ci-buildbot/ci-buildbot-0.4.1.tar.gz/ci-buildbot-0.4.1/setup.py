#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ci-buildbot",
    version='0.4.1',
    description="Slack client for reporting on CodePipeline runs",
    url="https://github.com/caltechads/ci-buildbot",
    author="Caltech IMSS ADS",
    author_email="imss-ads-staff@caltech.edu",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test", "bin", "*.pyc"]),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['aws', 'ecs', 'docker', 'devops'],
    entry_points={
        'console_scripts': ['buildbot = ci_buildbot.cli:main']
    },
    install_requires=[
        "slackclient >= 2.5.0",
        "docker >= 4.2.1",
        "gitpython >= 3.1.0",
        "giturlparse >= 0.9.2",
        "click >= 7.0",
        "jinja2 >= 2.11.1",
        "pydantic == 1.4",
        "pytz == 2019.1",
        "sh == 1.13.1"
    ],
)
