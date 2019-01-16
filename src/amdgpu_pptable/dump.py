import argparse
import ctypes
import json
import sys

from . import version_detect, version


def make_serializable(obj):
    if isinstance(obj, ctypes.Structure):
        return {field: make_serializable(getattr(obj, field)) for field, _ in obj._fields_}

    if isinstance(obj, ctypes.Array):
        return [make_serializable(e) for e in obj]

    return obj


def dump(pptable_file, output, indent=None):
    pptable = version_detect.parse(bytearray(pptable_file.read()))
    json.dump({k: make_serializable(v) for k, v in pptable._asdict().items()}, output, indent=indent)


def main(args=None):
    cmdline = argparse.ArgumentParser()
    cmdline.add_argument('pptable_file', type=argparse.FileType('rb'))
    cmdline.add_argument('-o', '--output', type=argparse.FileType('wt'), default=sys.stdout)
    cmdline.add_argument('--indent', type=int)
    cmdline.add_argument('--version', action='version', version=f'%(prog)s {version.version}')
    dump(**vars(cmdline.parse_args(args)))


if __name__ == '__main__':
    main()
