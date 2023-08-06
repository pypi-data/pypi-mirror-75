# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import io
import os

from setuptools import find_packages, setup

# 包元信息
NAME = 'feishu'
DESCRIPTION = 'python sdk for lark and feishu ( open.feishu.cn )'
URL = 'https://github.com/larksuite/feishu'
EMAIL = 'chyroc@bytedance.com'
AUTHOR = 'chyroc'

# 项目运行需要的依赖
REQUIRES = [

]

# 开发、测试过程中需要的依赖
DEV_REQUIRES = [

]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except IOError:
    long_description = DESCRIPTION

about = {}
with io.open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='lark',
    packages=find_packages(exclude=['__tool_open_docs', 'docs', 'tests']),
    install_requires=REQUIRES,
    tests_require=[
        'pytest>=4.0.0,<5.0.0',
        'pytest-cov',
    ],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    extras_require={
        ':python_version<"3.5"': [
            'typing>=3.6.4',
            'enum34>=1.1.0',
        ],
        'dev': DEV_REQUIRES,
    }
)