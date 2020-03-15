import setuptools


setuptools.setup(
    name='amdgpu-pptable',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    python_requires='>=3.6',
    use_scm_version={'write_to': 'src/amdgpu_pptable/version.py'}
)
