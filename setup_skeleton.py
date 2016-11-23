#!/usr/bin/env python

from __future__ import print_function
from argparse import ArgumentParser
import subprocess
import os
import urllib


def replace_in_file(filename, *tuples):
    """
    Replace `old` text in `filename` by `new`.
    """
    with open(filename) as fp:
        text = fp.read()
    for old, new in tuples:
        text = text.replace(old, new)
    with open(filename, 'w') as fp:
        fp.write(text)


def __main__():
    ap = ArgumentParser('setup_skeleton')
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('name', help='name of the python package', nargs='?')
    group.add_argument('--reset', '-r', action='store_true', help='reset the repository to HEAD')
    ap.add_argument('--author', '-a', help='author of the package', default='tillahoffmann')
    ap.add_argument('--version', '-v', default='0.1', help='version of the package')
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

        # Rename the package
        os.rename('python_skeleton', args.name)

        # Rename the environment
        replace_in_file('environment.yml', ('python_skeleton', args.name))
        replace_in_file('.travis.yml', ('python_skeleton', args.name))
        # Update the README
        replace_in_file('README.md', ('python_skeleton', args.name), ('tillahoffmann', args.author))
        # Update the test
        replace_in_file('tests/test_import.py', ('python_skeleton', args.name))
        replace_in_file('Makefile', ('python_skeleton', args.name))

        print("Replaced paths and contents.")

        url = 'https://github.com/%s/%s' % (args.author, args.name)
        try:
            urllib.request.urlopen(url)
            print("The repository %s/%s is public. Head to https://travis-ci.org to set up continuous integration." %
                  (args.author, args.name))
        except urllib.error.HTTPError:
            print("The repository %s/%s is private (or does not exist). Head to https://travis-ci.com to set up "
                  "continuous integration. You will have to update the status badge in README.md by hand. Sorry." %
                  (args.author, args.name))



if __name__ == '__main__':
    __main__()
