from setuptools import setup, find_packages

setup(
    name             = 'pyrawdatamanage',
    version          = '1.1',
    description      = 'Handling Record move and delete raw data history',
    author           = 'Seho Choi',
    author_email     = 'seho@histogenetics.com',
    url              = '',
    download_url     = '',
    install_requires = [ ],
    packages         = find_packages(exclude = ['docs', 'tests*']),
    classifiers      = [
        'Programming Language :: Python :: 2.7',
    ]
)