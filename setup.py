"""
Installation Script
"""

from setuptools import setup, find_packages

# Read README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read requirements.txt file
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="p_wave_picker",
    version="0.1.0",
    description='P-wave First Arrival Phase Picking System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jiachen Hu',
    author_email='jiachen.hu@zju.edu.cn',
    url='https://github.com/hhhjjjcc/JC-Phase-Picker.git',
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
        'Documentation': 'https://github.com/hhhjjjcc/JC-Phase-Picker.git/docs',
        'Source': 'https://github.com/hhhjjjcc/JC-Phase-Picker.git',
        'Tracker': 'https://github.com/hhhjjjcc/JC-Phase-Picker.git/issues',
    },
) 