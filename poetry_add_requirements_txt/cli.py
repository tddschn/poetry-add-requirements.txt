#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-01
Purpose: Add dependencies specified in requirements.txt to your Poetry project
"""

import argparse
import encodings

import subprocess
from pathlib import Path
from charset_normalizer import detect


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
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

    return parser.parse_args()


def poetry_add(dep: str, dev: bool = False):
    """Add dependency with Poetry"""
    cmd = ['poetry', 'add']
    if dev:
        cmd.append('-D')
    cmd.append(dep)
    print(f'Running {" ".join(cmd)}')
    cp = subprocess.run(cmd)
    if cp.returncode != 0:
        raise Exception(f'Failed to add dependency {dep} with {" ".join(cmd)}')


def process_req_file(req_file: Path, dev: bool):
    b = req_file.read_bytes()
    encoding: str = detect(b)['encoding']  # type: ignore
    for line in b.decode(encoding).splitlines():
        dep = line.strip()
        if dep:
            poetry_add(dep, dev)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    req_files = args.requirements_txt_file
    dev = args.dev
    if isinstance(req_files, Path):
        req_files = [req_files]
    for req_file in req_files:
        process_req_file(req_file, dev)


# --------------------------------------------------
if __name__ == '__main__':
    main()
