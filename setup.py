"""
安装脚本
"""

from setuptools import setup, find_packages

# 读取README文件
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取requirements.txt文件
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="p_wave_picker",
    version="0.1.0",
    description='P波初至震相拾取系统',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='XXX',
    author_email='xxx@example.com',
    url='https://github.com/xxx/p_wave_picker',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "obspy>=1.4.0",
        "matplotlib>=3.5.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
    ],
    entry_points={
        'console_scripts': [
            'p_wave_picker=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    python_requires=">=3.7",
    keywords='seismology, phase picking, P-wave',
    project_urls={
        'Documentation': 'https://github.com/xxx/p_wave_picker/docs',
        'Source': 'https://github.com/xxx/p_wave_picker',
        'Tracker': 'https://github.com/xxx/p_wave_picker/issues',
    },
) 