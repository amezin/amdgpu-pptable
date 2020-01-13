import argparse
import io
import logging
import os
import tokenize

import ctypeslib.codegen.codegenerator
import ctypeslib.codegen.typedesc


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


def generate_ctypes(header_file, py_file, cpp_flags):
    logging.info("Generating %s from %s", py_file, header_file)

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
    bytes = tokenize.untokenize(rewrite_ctypes_little_endian(bytes_buffer.readline))

    with open(py_file, 'wb') as outfile:
        outfile.write(bytes)


def run(kernel_dir, log_level):
    logging.basicConfig(level=log_level)

    kernel_dir = os.path.abspath(kernel_dir)
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'amdgpu_pptable', 'generated')

    header_file = os.path.join(kernel_dir, 'drivers/gpu/drm/amd/powerplay/hwmgr/vega10_pptable.h')
    includes = [
        os.path.join(kernel_dir, 'drivers/gpu/drm/amd/include/atom-types.h'),
        os.path.join(kernel_dir, 'drivers/gpu/drm/amd/include/atomfirmware.h')
    ]
    py_file = os.path.join(out_dir, 'vega10_pptable.py')

    cpp_flags = ['-include', 'stdint.h']
    for inc in includes:
        cpp_flags.extend(('-include', inc))

    generate_ctypes(header_file, py_file, cpp_flags)

    header_file = os.path.join(kernel_dir, 'drivers/gpu/drm/amd/powerplay/hwmgr/pptable_v1_0.h')
    py_file = os.path.join(out_dir, 'pptable_v1_0.py')
    includes = [
        os.path.join(kernel_dir, 'drivers/gpu/drm/amd/include/atom-types.h'),
        os.path.join(kernel_dir, 'drivers/gpu/drm/amd/include/atombios.h')
    ]
    cpp_flags = ['-include', 'stdint.h']
    for inc in includes:
        cpp_flags.extend(('-include', inc))

    generate_ctypes(header_file, py_file, cpp_flags)

    header_file = os.path.join(kernel_dir, 'drivers/gpu/drm/amd/powerplay/inc/smu_v11_0_pptable.h')
    py_file = os.path.join(out_dir, 'smu_v11_0_pptable_navi10.py')
    includes = [
        os.path.join(kernel_dir, 'drivers/gpu/drm/amd/include/atom-types.h'),
        os.path.join(kernel_dir, 'drivers/gpu/drm/amd/include/atomfirmware.h'),
        os.path.join(kernel_dir, 'drivers/gpu/drm/amd/powerplay/inc/smu11_driver_if_navi10.h')
    ]
    cpp_flags = ['-include', 'stdint.h']
    for inc in includes:
        cpp_flags.extend(('-include', inc))

    generate_ctypes(header_file, py_file, cpp_flags)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Python modules from kernel headers"
    )
    parser.add_argument(
        "-k", "--kernel-dir", required=True, help="kernel source directory"
    )
    parser.add_argument(
        "--log-level", type=logging.getLevelName, default=logging.INFO
    )
    run(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
