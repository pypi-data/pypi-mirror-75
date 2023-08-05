#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="wy-sentry-dingding",
    version='0.0.7',
    author='404',
    author_email='404@gmail.com',
    url='https://404.com',
    description='send sentry messages to dingding',
    license='MIT',
    keywords='sentry dingding',
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'sentry>=9.0.0',
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'sentry_dingding = sentry_dingding.plugin:DingDingPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "License :: OSI Approved :: MIT License",
    ]
)
