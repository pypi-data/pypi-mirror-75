from setuptools import setup, find_packages
import xmem

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='xmem',
    version=xmem.__version__,
    author='Schicksal',
    description='A simple, light, easy-to-use, and extensible memory module',
    author_email='mhaisham79@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],

    license="MIT license",
    keywords='memory storage json pickle extensible light',

    url='https://github.com/mHaisham/xmem',
    packages=find_packages(),
    python_requires='>=3.6'
)
