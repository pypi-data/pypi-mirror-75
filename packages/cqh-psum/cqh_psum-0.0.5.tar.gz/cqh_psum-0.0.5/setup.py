import io
import os
import re

from setuptools import find_packages
from setuptools import setup

proj_name = 'cqh_psum'
_dir = os.path.dirname(os.path.abspath(__file__))
init_path = os.path.join(_dir, proj_name, '__init__.py')


def update_d(file_path):
    d = {}
    code = open(file_path).read()
    code = compile(code, '<string>', 'exec', dont_inherit=True)
    exec(code, d, d)
    return d


init_d = update_d(init_path)


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name=proj_name,
    version=init_d['__version__'],
    url="https://github.com/kragniz/cookiecutter-pypackage-minimal",
    license='MIT',

    author="cqh",

    description="progress sum memory for name",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=['psutil', 'prettytable'],
    entry_points={
        "console_scripts": [
            "cqh_psum=cqh_psum.run:main",
        ],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
