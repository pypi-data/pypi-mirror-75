from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


import bibtexentryparser




setup(
    name='bibtexentryparser',
    version=bibtexentryparser.__version__,
    description='Python module to parse BibTeX entries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #long_description=long_description,
    author='Sonja Stuedli',
    author_email='scythja@gmail.com',
    url='https://github.com/scythja123/python-bitexentryparser',
    license= 'LGPLv3 or BSD',
    packages=find_packages(where=here),
    install_requires=[],
    python_requires='>=3',
    platforms=['any']
)
