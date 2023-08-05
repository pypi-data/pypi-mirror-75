from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


import python_to_latex as p2l


setup(
    name='python_to_latex',
    version=p2l.__version__,
    description='Python module to facilitate input in LaTex from Python scripts',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #long_description=long_description,
    author=p2l.__authors__,
    author_email=p2l.__author_emails__,
    url='https://github.com/scythja123/TODO',
    license= 'GPLv3',
    packages=find_packages(where=here),
    install_requires=[],
    python_requires='>=3',
    platforms=['any']
)
