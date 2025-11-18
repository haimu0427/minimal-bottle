#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Minimal Bottle 安装脚本
"""

from setuptools import setup
import os

# 读取README文件
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='minimal-bottle',
    version='0.1.0',
    description='A stripped-down version of Bottle web framework with zero dependencies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Minimal Bottle Team',
    author_email='contact@minimalbottle.org',
    url='https://github.com/yourusername/minimal-bottle',
    py_modules=['bottle_minimal'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='web framework wsgi bottle minimal lightweight',
    python_requires='>=3.6',
    install_requires=[],  # 零依赖
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'flake8>=3.8.0',
            'black>=21.0.0',
        ],
        'test': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'minimal-bottle=examples.basic:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/minimal-bottle/issues',
        'Source': 'https://github.com/yourusername/minimal-bottle',
        'Documentation': 'https://github.com/yourusername/minimal-bottle#readme',
    },
    include_package_data=True,
    zip_safe=False,
)
