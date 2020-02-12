import setuptools


with open('README.rst') as fp:
    long_description = fp.read()


setuptools.setup(
    name='amdgpu-pptable',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['PyQt5'],
    setup_requires=['setuptools_scm', 'setuptools-scm-git-archive'],
    entry_points={
        'console_scripts': ['amdgpu-pptable-to-json=amdgpu_pptable.dump:main'],
        'gui_scripts': ['amdgpu-pptable-editor=amdgpu_pptable.gui:main']
    },
    python_requires='>=3.6',
    use_scm_version={'write_to': 'src/amdgpu_pptable/version.py'},

    keywords=['amdgpu', 'radeon', 'powerplay'],
    url='https://github.com/amezin/powerplay-table-editor',
    author='Aleksandr Mezin',
    author_email='mezin.alexander@gmail.com',
    maintainer='Aleksandr Mezin',
    maintainer_email='mezin.alexander@gmail.com',
    description='A Python library that converts AMD powerplay tables to ctypes structs, and a Qt GUI editor for these struct objects',
    long_description=long_description,
    long_description_content_type='text/x-rst'
)
