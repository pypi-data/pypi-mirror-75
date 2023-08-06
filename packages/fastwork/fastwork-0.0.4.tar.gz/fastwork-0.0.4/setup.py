# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastwork",
    version="0.0.4",
    author="soaringsoul",
    author_email="951683309@qq.com",
    description="an useful tool for ending your boring work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xugongli/fastwork.git",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules', ],
    python_requires='>=3.5',
    install_requires=[
		'xlsxwriter>=1.2.0',
        'openpyxl>=3.0.4',
        'pandas>=1.0.5',
        'xlrd>=1.2.0'
    ],
)
