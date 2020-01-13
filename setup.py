import setuptools


setuptools.setup(
    name='amdgpu-pptable',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['PyQt5'],
    setup_requires=['pytest-runner', 'setuptools_scm', 'setuptools_scm_git_archive'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['amdgpu-pptable-to-json=amdgpu_pptable.dump:main'],
        'gui_scripts': ['amdgpu-pptable-editor=amdgpu_pptable.gui:main']
    },
    python_requires='>=3.6',
    use_scm_version={'write_to': 'src/amdgpu_pptable/version.py'}
)
