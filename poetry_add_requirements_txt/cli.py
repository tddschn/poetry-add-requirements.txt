#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-01
Purpose: Add dependencies specified in requirements.txt file(s) to your Poetry project
"""

import argparse
from pathlib import Path
from poetry_add_requirements_txt import __version__, __app_name__
from poetry_add_requirements_txt.utils import preprocess_line

# PYPI_NAME_PATTERN = r'([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])'


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description='Add dependencies specified in requirements.txt to your Poetry project',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        'requirements_txt_file',
        metavar='requirements.txt file(s)',
        help='Path(s) to your requirements.txt file(s)',
        type=Path,
        nargs='*',
        default=Path('requirements.txt'),
    )

    parser.add_argument(
        '-D', '--dev', help='Add to development dependencies', action='store_true'
    )

    parser.add_argument(
        '-I',
        '--ignore-version-requirements',
        help='Ignore dependency version requirements in requirements.txt file(s)',
        action='store_true',
    )

    parser.add_argument(
        '-V', '--version', action='version', version=f'%(prog)s {__version__}'
    )

    return parser.parse_args()


def poetry_add(dep: str, dev: bool = False):
    """Add dependency with Poetry"""
    import subprocess

    cmd = ['poetry', 'add']
    if dev:
        cmd.append('-D')
    cmd.append(dep)
    print(f'Running {" ".join(cmd)}')
    cp = subprocess.run(cmd)
    if cp.returncode != 0:
        raise Exception(f'Failed to add dependency {dep} with {" ".join(cmd)}')


def process_req_file(req_file: Path, dev: bool, ignore_version_requirements: bool):
    print(f'Reading requirements file: {str(req_file)}')
    b = req_file.read_bytes()
    from charset_normalizer import detect

    encoding: str = detect(b)['encoding']  # type: ignore
    for line in b.decode(encoding).splitlines():
        dep = preprocess_line(line)
        if dep:
            if ignore_version_requirements:
                import re

                # https://peps.python.org/pep-0508/
                # pypi_name_pattern = re.compile(r'([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])', re.IGNORECASE)
                match = re.match(r'([\w][\w\d\._-]*)', dep)
                if match is None or match.groups()[0] == '':
                    continue
                dep = match.groups()[0]
            poetry_add(dep, dev)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    req_files = args.requirements_txt_file
    dev = args.dev
    ignore_version_requirements = args.ignore_version_requirements
    if isinstance(req_files, Path):
        req_files = [req_files]
    for req_file in req_files:
        process_req_file(req_file, dev, ignore_version_requirements)


# --------------------------------------------------
if __name__ == '__main__':
    main()
