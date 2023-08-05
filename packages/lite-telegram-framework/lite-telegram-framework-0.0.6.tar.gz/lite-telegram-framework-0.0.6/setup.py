from setuptools import setup, find_packages
import sys


MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def read(path):
    with open(path, 'r', encoding='utf-8') as fh:
        return fh.read()


setup(
    python_requires='>=3.7',
    name='lite-telegram-framework',
    version=read('VERSION').strip(),
    description='Lite framework for writing telegram bots',
    url='http://github.com/codeomatic/lite-telegram-framework',
    author='Denis Nikolskiy',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['requests'],
    include_package_data=True,
    zip_safe=False,
    keywords='telegram api telegrambot',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Source': 'https://github.com/codeomatic/lite-telegram-framework',
    },
)
