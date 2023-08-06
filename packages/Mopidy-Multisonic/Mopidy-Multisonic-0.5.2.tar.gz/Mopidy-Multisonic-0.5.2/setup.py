import re
from setuptools import setup, find_packages
from pypandoc import convert_text

def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    print(metadata)
    return metadata['version']

setup(
    name='Mopidy-Multisonic',
    version=get_version('mopidy_multisonic/__init__.py'),
    url='https://sr.ht/~reedwade/mopidy-multisonic/',
    license='Apache License, Version 2.0',
    author='ReedWade',
    author_email='<reedwade@misterbanal.net>',
    description='A mopidy backend provider for multisonic services',
    long_description=convert_text(open('README.md').read(), format='md', to='rst'),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 0.14',
        'Pykka >= 1.1',
    ],
    entry_points={
        'mopidy.ext': [
            'multisonic = mopidy_multisonic:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
