from distutils.core import setup

version = '0.0.16'
name = 'globals'
url = 'https://github.com/SamuelJansen/globals/'

setup(
  name = name,
  packages = ['api','src'],
  version = version,
  license='MIT',
  description = 'import package handler',
  author = 'Samuel Jansen',
  author_email = 'samuel.jansenn@gmail.com',
  url = url,
  download_url = f'{url}archive/v{version}.tar.gz',
  keywords = ['global', 'python global package', 'python package manager', 'global package manager'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
  ]
)
