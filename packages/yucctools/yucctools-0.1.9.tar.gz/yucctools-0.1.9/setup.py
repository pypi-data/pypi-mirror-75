from setuptools import setup

import shutil
from pathlib import Path

# Remove stale transformers.egg-info directory to avoid https://github.com/pypa/pip/issues/5466
stale_egg_info = Path(__file__).parent / "yucctools.egg-info"
if stale_egg_info.exists():
    shutil.rmtree(stale_egg_info)

stale_dist = Path(__file__).parent / "dist"
if stale_dist.exists():
    shutil.rmtree(stale_dist)



setup(name='yucctools',
        version='0.1.9',
        description='一些常用的通用的工具, 比如日志记录工具',
        long_description=open('README.md', 'r', encoding='utf-8').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/yucc2018/yucctools',
        author='Chen-Chen Yu',
        author_email='6506666@gmail.com',
        license='MIT',
        packages=['yucctools'],
        zip_safe=False)

