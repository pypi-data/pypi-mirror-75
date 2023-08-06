from setuptools import dist, setup, Extension
# To compile and install locally run "python setup.py build_ext --inplace"
# To install library to Python site-packages run "python setup.py build_ext install"


setup_requires=[
    'setuptools>=18.0',
    'cython>=0.27.3',
    'numpy',
]
dist.Distribution().fetch_build_eggs(setup_requires)

import numpy as np

ext_modules = [
    Extension(
        'iMICSdset_utils._mask',
        sources=['./common/maskApi.c', 'iMICSdset_utils/_mask.pyx'],
        include_dirs=['./common', np.get_include()],
        extra_compile_args=['-Wno-cpp', '-Wno-unused-function', '-std=c99'],
    )
]

setup(
    name='iMICSdset_utils',
    description='Official APIs for the MS-COCO dataset',
    packages=['iMICSdset_utils'],
    package_dir = {'iMICSdset_utils': 'iMICSdset_utils'},
    setup_requires=setup_requires,
    install_requires=[
        'setuptools>=18.0',
        'cython>=0.27.3',
        'matplotlib>=2.1.0'
    ],
    version='1.0.0',
    ext_modules= ext_modules,
    author="Ernest (Khashayar) Namdar",
    author_email="ernest.namdar@utoronto.ca"
)
