import os
import re
from setuptools import setup, find_packages


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([a-zA-Z0-9.]+)['"]''')


def get_version():
    """Return the version number"""
    init = open(os.path.join(ROOT, 'ospclientsdk', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


def get_long_description():
    """Returns README.md content."""
    return open("README.md", "r").read()

setup(
    name='ospclientsdk',
    version=get_version(),
    description="An SDK like wrapper around the openstackclient.",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author="Danny Baez",
    url="https://github.com/Dannyb48/ospclientsdk",
    author_email='danny.baez.jr@gmail.com',
    license='GPLv3',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: OpenStack',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    install_requires=[
        'openstackclient',
        'PyYaml'
    ],
    extras_require={
        'remote_shell': ['plumbum']
    }
)
