from setuptools import setup, find_namespace_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='plotting-framework-aymatveev',
    version='0.2',
    description='Demo plotting framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aymatveev/plotting_framework',
    author='aymatveev',
    author_email='aymatveev@itmo.ru',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    python_requires='>=3, <4',
    install_requires=[],
    extras_require={'dev': ['testing-framework-aymatveev @ git+https://github.com/aymatveev/testing_framework.git']},
)
