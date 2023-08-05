"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

setup(
    name='orbis-new',
    version='0.0.2',
    description='Real time ORBIS data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/donglai96/ORBIS_new',
    packages=find_packages(),
    author='Donglai Ma',
    author_email='dma96@atmos.ucla.edu',
    license='MIT',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.7',
                 ],
    keywords='predict radiation-belt',

    #packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    #install_requires=['numpy','mechanize','tensorflow >=2.0','scipy','pandas'],
    python_requires='>=3.5',
    include_package_data=True,
)