from setuptools import setup, find_packages

setup(
    name             = 'pymarktex',
    version          = '1.4.6',
    description      = 'Will convert a markdown text file to a fancy PDF document',
    license          = 'MIT',
    url              = 'http://github.com/xapple/pymarktex/',
    author           = 'Lucas Sinclair',
    author_email     = 'lucas.sinclair@me.com',
    packages         = find_packages(),
    scripts          = ['scripts/pymarktex'],
    install_requires = ['plumbing>=2.8.1', 'autopaths>=1.4.2', 'pystache>=0.5.4',
                        'pbs3'],
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    include_package_data = True,
)