from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

version = {}
ver_text = (here / 'pytris' / 'version.py').read_text(encoding='utf-8')
exec(ver_text, version)

setup(
    name='pyTRIS',
    version=version['__version__'],
    description=(
        'Simple no-dependencies API wrapper for Highways England\'s WebTRIS '
        'Traffic Flow API'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/asongtoruin/pyTRIS',
    author='Adam Ruszkowski',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='transport',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    project_urls={
        'Documentation': 'https://asongtoruin.github.io/pyTRIS/',
        'Source': 'https://github.com/asongtoruin/pyTRIS/',
    },
)