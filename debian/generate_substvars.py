#!/usr/bin/env python3

import email.parser


def escape_value(value):
    return value.replace('\n', '${Newline}')


def generate_substvars_to_path(pkg_info_file):
    for key, value in email.parser.HeaderParser().parse(pkg_info_file).items():
        print(f'setuptools:{key}={escape_value(value)}')


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('pkg_info_file', type=argparse.FileType('r'))
    generate_substvars_to_path(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
