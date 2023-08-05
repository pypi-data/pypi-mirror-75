#!/usr/bin/env python
# coding: utf-8
"""
filelib.py
"""

import os
import re

# https://github.com/semver/semver/pull/460/files
VALID_SEMVER = '(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'


def is_valid_semver(semver_string):
    return bool(re.match(VALID_SEMVER, semver_string))


def possible_file_paths():
    """
    Return a list of all the possible locations the version string could be in
    Possibilities:
      - pkg/pkg/_version.py
      - pkg/pkg/__init__.py
      - pkg/VERSION
      - pkg/VERSION.py
      - pkg/VERSION.txt
      - pkg/setup.py
    """
    # This will get current dir name
    # Useful because we need to be in the package repos root dir
    # and the source should be in another dir with the same name
    pkg_name = os.path.basename(os.getcwd())

    return [
        'pyproject.toml',
        'VERSION.txt',
        'setup.py',
        '%s/_version.py' % pkg_name,
        '%s/VERSION' % pkg_name,
        '%s/VERSION.py' % pkg_name,
        '%s/VERSION.txt' % pkg_name,
        '%s/__init__.py' % pkg_name,
        '_version.py',
        'VERSION',
        'VERSION.py',
    ]


def search_for_possible_files(filepath=None):
    """
    Will search for each file that may contain the version string and returns that list
    """
    files_that_exist = []

    if filepath is None:
        for file in possible_file_paths():
            if os.path.exists(file):
                files_that_exist.append(file)

    return files_that_exist


def search_file_for_valid_semver(filepath):
    """
    Take a file and look for the version string
    """
    ret = None

    with open(filepath, 'r') as f:
        for line in f.readlines():
            if line == '':
                continue
            m = re.search(VALID_SEMVER, line)

            if m:
                ret = m.group(0)
                break

    return ret


def search_each_existing_file(files):
    """
    Takes a List of files that exist and searches for the first valid semver string, then
    returns the string and the name of the file it was found in
    """
    ret = None, None

    for file in files:
        n = search_file_for_valid_semver(file)

        if n:
            ret = n, file
            break

    return ret


def modify_file_with_new_version_string(file, old, new):
    """
    Takes a file path and the old and new version strings to do a replacement
    """
    with open(file, 'r') as f:
        file_contents = f.read()

    if old in file_contents:
        file_contents = file_contents.replace(old, new, 1)

        with open(file, 'w') as f:
            f.write(file_contents)
