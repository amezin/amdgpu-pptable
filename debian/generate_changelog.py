#!/usr/bin/env python3

import email.parser
import sys

import debian.changelog


def generate_changelog(pkg_info_file):
    metadata = email.parser.HeaderParser().parse(pkg_info_file)

    changelog = debian.changelog.Changelog()
    changelog.new_block(
        package=metadata['Name'],
        version=metadata['Version'],
        distributions='unstable',
        author='%s <%s>' % debian.changelog.get_maintainer(),
        date=debian.changelog.format_date(localtime=False)
    )
    return changelog


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('pkg_info_file', type=argparse.FileType('r'))
    generate_changelog(**vars(parser.parse_args())).write_to_open_file(sys.stdout)


if __name__ == '__main__':
    main()
