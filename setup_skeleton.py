#!/usr/bin/env python

from __future__ import print_function
from argparse import ArgumentParser
import subprocess


def __main__():
    ap = ArgumentParser('setup_skeleton')
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('name', help='name of the python package', nargs='?')
    group.add_argument('--reset', '-r', action='store_true', help='reset the repository to HEAD')
    ap.add_argument('--author', '-a', help='author of the package', default='Till Hoffmann')
    ap.add_argument('--version', '-v', default='0.1')
    args = ap.parse_args()

    if args.reset:
        answer = input('Do you really want to reset the repository? [y/N]\n')
        if answer.lower() in ('y', 'yes'):
            subprocess.run(['git', 'reset', '--hard'])
            print("Reset repository.")
        else:
            print("Did not reset repository.")
    else:
        # Define the template for setup.py
        template = """from setuptools import setup, find_packages


setup(
    name='{name}',
    version='{version}',
    author='{author}',
    packages=find_packages(),
)
"""
        setup_py = template.format(name=args.name, version=args.version, author=args.author)
        with open('setup.py', 'w') as fp:
            fp.write(setup_py)

        print("Created setup.py.")



if __name__ == '__main__':
    __main__()
