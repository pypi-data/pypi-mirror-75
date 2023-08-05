import re
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

CURDIR = dirname(abspath(__file__))

with open("README.md", "r", encoding='utf-8') as fh:
    LONG_DESCRIPTION = fh.read()

with open(join(CURDIR, 'PuppeteerPercy', '__init__.py'), encoding='utf-8') as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)


setup(
    name="robotframework-puppeteer-percy",
    version=VERSION,
    author="QA Hive Co.,Ltd",
    author_email="support@qahive.com",
    description="Puppeteer Percy Library is a puppeteer percy client library for robot framework",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license="Apache License 2.0",
    url='https://github.com/qahive/robotframework-puppeteer-percy',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    keywords='robotframework puppeteer percy web-testing automation',
    platforms='any',
    install_requires=[
        'robotframework>=3.2.1',
        'pyppeteer>=0.2.2',
        'requests>=2'
    ],
    zip_safe=False
)
