import io
import os
import tokenize

import setuptools
import distutils.core


class GenerateCtypes(distutils.core.Command):

    description = "Generate Python modules from kernel headers"

    user_options = [
        ('kernel-dir=', 'k', "kernel source directory"),
        ('force', 'f', "forcibly build everything (ignore file timestamps)"),
    ]

    boolean_options = ['force']

    def __init__(self, dist):
        super().__init__(dist)
        self.kernel_dir = None
        self.out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'amdgpu_pptable', 'generated')

    def initialize_options(self):
        self.force = False
        self.kernel_dir = None

    def finalize_options(self):
        if not self.kernel_dir:
            raise distutils.core.DistutilsOptionError("kernel-dir is required")

        self.ensure_dirname('kernel_dir')
        self.kernel_dir = os.path.abspath(self.kernel_dir)

    @staticmethod
    def rewrite_ctypes_little_endian(readline):
        prev_tokens = [None, None]

        def rewrite_token(token):
            if prev_tokens[0] is None or prev_tokens[1] is None:
                return token

            if prev_tokens[0].string != '.' or prev_tokens[1].string != 'ctypes':
                return token

            if token.string == 'Structure':
                return (token.type, 'LittleEndianStructure') + token[2:]
            elif token.string == 'Union':
                return (token.type, 'LittleEndianUnion') + token[2:]
            else:
                return token

        for token in tokenize.tokenize(readline):
            yield rewrite_token(token)

            prev_tokens[1] = prev_tokens[0]
            prev_tokens[0] = token

    def generate_ctypes(self, header_file, py_file, cpp_flags):
        import ctypeslib.codegen.codegenerator
        import ctypeslib.codegen.typedesc

        buffer = io.StringIO()
        ctypeslib.codegen.codegenerator.generate_code([header_file], buffer,
                                                      types=(ctypeslib.codegen.typedesc.Alias,
                                                             ctypeslib.codegen.typedesc.Structure,
                                                             ctypeslib.codegen.typedesc.Variable,
                                                             ctypeslib.codegen.typedesc.Enumeration,
                                                             ctypeslib.codegen.typedesc.Function,
                                                             ctypeslib.codegen.typedesc.Macro,
                                                             ctypeslib.codegen.typedesc.Typedef,
                                                             ctypeslib.codegen.typedesc.Union),
                                                      filter_location=True,
                                                      flags=cpp_flags)

        bytes_buffer = io.BytesIO(buffer.getvalue().encode())
        bytes = tokenize.untokenize(self.rewrite_ctypes_little_endian(bytes_buffer.readline))

        with open(py_file, 'wb') as outfile:
            outfile.write(bytes)

    def run(self):
        header_file = os.path.join(self.kernel_dir, 'drivers/gpu/drm/amd/powerplay/hwmgr/vega10_pptable.h')
        includes = [
            os.path.join(self.kernel_dir, 'drivers/gpu/drm/amd/include/atom-types.h'),
            os.path.join(self.kernel_dir, 'drivers/gpu/drm/amd/include/atomfirmware.h')
        ]
        py_file = os.path.join(self.out_dir, 'vega10_pptable.py')

        cpp_flags = ['-include', 'stdint.h']
        for inc in includes:
            cpp_flags.extend(('-include', inc))

        self.make_file([header_file] + includes + [__file__],
                       py_file,
                       self.generate_ctypes,
                       (header_file, py_file, cpp_flags))


setuptools.setup(
    name='amdgpu-pptable',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['PyQt5'],
    setup_requires=['pytest-runner', 'ctypeslib2'],
    tests_require=['pytest'],
    cmdclass={
        'generate_ctypes': GenerateCtypes
    },
    entry_points={
        'console_scripts': ['amdgpu-pptable-to-json=amdgpu_pptable.dump:main'],
        'gui_scripts': ['amdgpu-pptable-editor=amdgpu_pptable.gui:main']
    },
    python_requires='>=3'
)
