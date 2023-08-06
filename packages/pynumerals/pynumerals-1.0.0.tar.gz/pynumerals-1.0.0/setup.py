from setuptools import setup, find_packages


setup(
    name='pynumerals',
    version='1.0.0',
    license='Apache 2.0',
    description='Helper library for numeralbank projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    author='Hans-Jörg Bibiko, Christoph Rzymski, Robert Forkel',
    keywords='data',
    author_email='lingweb@shh.mpg.de',
    url='https://github.com/numeralbank/pynumerals',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.5',
    install_requires=[
        'attr',
        'beautifulsoup4>=4.6.3',
        'clldutils',
        'python-levenshtein',
        'fuzzywuzzy',
    ],
    extras_require={
        'dev': ['flake8', 'wheel', 'twine'],
        'test': [
            'mock',
            'pytest>=5.4',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'pyglottolog>=3.2.2',
        ],
    },
)
