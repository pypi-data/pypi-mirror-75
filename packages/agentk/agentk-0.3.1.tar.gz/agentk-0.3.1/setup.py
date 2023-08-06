"""
Packaging of the agentk tool.

For dev purposes: `pip install -e .`

Also see Makefile.
"""
import os
from setuptools import setup, find_packages


def get_version():
    with open(os.path.join(os.path.dirname(__file__), 'k')) as f:
        for line in f.read().split("\n"):
            if '__version__' in line:
                line = line[len('__version__ = "'):]
                return line[:line.index('"')]
        raise Exception("Failed to parse version.")


def get_readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


setup(
    name='agentk',
    version=get_version(),
    url='https://gitlab.com/kubic-ci/k',
    author='Yauhen Yakimovich',
    author_email='eugeny.yakimovitch@gmail.com',
    description='"AGENT" K is a complete minimalistic kubectl "doner"-wrap',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'sh>=1.12.13', 'pick>=0.6.4', 'clint>=0.5.1',
        'PyYAML>=5.1.2', 'windows-curses>=2.0 ; platform_system=="Windows"',
        'pbs==0.110 ; platform_system=="Windows"'],
    scripts=['k', 'k.bat'],
    license='MIT',
    download_url='https://gitlab.com/kubic-ci/k/-/archive/master/k-master.zip',
)
