import setuptools


with open('README.rst') as fp:
    long_description = fp.read()


setuptools.setup(
    name='amdgpu-pptable',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    python_requires='>=3.6',
    use_scm_version={'write_to': 'src/amdgpu_pptable/version.py'},
    description='AMDGPU PowerPlay table parser',
    long_description=long_description,
    url='https://github.com/amezin/amdgpu-pptable',
    keywords='amdgpu radeon powerplay',
    author='Aleksandr Mezin',
    author_email='mezin.alexander@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware'
    ]
)
