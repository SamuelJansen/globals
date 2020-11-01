from distutils.core import setup
import os

version = '0.0.43-6'
name = 'globals'
url = f'https://github.com/SamuelJansen/{name}/'

OS_SEPARATOR = os.path.sep

setup(
    name = name,
    packages = [
        name,
        f'{name}{OS_SEPARATOR}api',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}src',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}src{OS_SEPARATOR}service'
    ],
    version = version,
    license = 'MIT',
    description = 'import package handler',
    author = 'Samuel Jansen',
    author_email = 'samuel.jansenn@gmail.com',
    url = url,
    download_url = f'{url}archive/v{version}.tar.gz',
    keywords = ['global', 'python global package', 'python package manager', 'global package manager'],
    install_requires = [],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
    ]
)
