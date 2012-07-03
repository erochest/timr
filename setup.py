#!/usr/bin/env python

from distutils.core import setup

setup(
        name='timr',
        version='0.1.0',
        description='Profiling web requests.',
        author='Eric Rochester',
        author_email='erochest@virginia.edu',
        url='https://github.com/erochest/timr',
        download_url='https://github.com/downloads/erochest/timr/timr-0.1.0.tar.gz',
        license='Apache 2.0',

        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Software Development',
            ],

        requires=[
            'requests',
            ],

        packages=[
            'timrlib',
            ],
        py_modules=[
            ],
        scripts=[
            'timr',
            ],

        )
