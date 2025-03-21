#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-01
Purpose: Add dependencies specified in requirements.txt file(s) to your Poetry project
"""

import argparse
from pathlib import Path
from poetry_add_requirements_txt import __version__, __app_name_uv__
from poetry_add_requirements_txt.utils import preprocess_line

# PYPI_NAME_PATTERN = r'([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])'


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        prog=__app_name_uv__,
        description="Add dependencies specified in requirements.txt to your UV project",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "requirements_txt_file",
        metavar="requirements.txt file(s)",
        help="Path(s) to your requirements.txt file(s)",
        type=Path,
        nargs="*",
        default=Path("requirements.txt"),
    )

    parser.add_argument(
        "-D", "--dev", help="Add to development dependencies", action="store_true"
    )

    parser.add_argument(
        "-I",
        "--ignore-version-requirements",
        help="Ignore dependency version requirements in requirements.txt file(s)",
        action="store_true",
    )

    parser.add_argument(
        "-i", "--ignore-errors", help="Ignore errors", action="store_true"
    )

    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Dry run, do not add dependencies"
    )

    parser.add_argument(
        "-p",
        "--poetry-args",
        dest="poetry_args",
        help="Additional arguments to pass to uv, put this at the END of the command",
        nargs=argparse.REMAINDER,
    )

    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser.parse_args()


def poetry_add(
    dep: str,
    dev: bool = False,
    poetry_extra_args: list | None = None,
    dry_run: bool = False,
):
    """Add dependency with Poetry"""
    import subprocess

    cmd = ["uv", "add"]
    if dev:
        cmd.append("--dev")
    cmd.append(dep)
    if poetry_extra_args:
        cmd.extend(poetry_extra_args)
    print(f"Running {' '.join(cmd)}")
    if dry_run:
        return
    cp = subprocess.run(cmd)
    if cp.returncode != 0:
        raise Exception(f"Failed to add dependency {dep} with {' '.join(cmd)}")


def process_req_file(
    req_file: Path,
    dev: bool,
    ignore_version_requirements: bool,
    ignore_errors: bool,  # New parameter
    poetry_extra_args: list | None = None,
    dry_run: bool = False,
):
    print(f"Reading requirements file: {str(req_file)}")
    b = req_file.read_bytes()
    from charset_normalizer import detect

    encoding: str = detect(b)["encoding"]  # type: ignore
    for line in b.decode(encoding).splitlines():
        try:
            dep = preprocess_line(line)
            if dep:
                if ignore_version_requirements:
                    import re

                    match = re.match(r"([\w][\w\d\._-]*)", dep)
                    if match is None or match.groups()[0] == "":
                        continue
                    dep = match.groups()[0]
                poetry_add(dep, dev, poetry_extra_args, dry_run)
        except Exception as e:
            if ignore_errors:
                print(f"Error processing '{line}': {e}")
            else:
                raise


def main():
    """Make a jazz noise here"""

    args = get_args()
    req_files = args.requirements_txt_file
    dev = args.dev
    ignore_version_requirements = args.ignore_version_requirements
    ignore_errors = args.ignore_errors  # Capture the ignore_errors flag
    # poetry_extra_args = (
    #     args.poetry_args[1:] if args.poetry_args and args.poetry_args[0] == "--" else []
    # )
    poetry_extra_args = args.poetry_args

    if isinstance(req_files, Path):
        req_files = [req_files]
    for req_file in req_files:
        process_req_file(
            req_file,
            dev,
            ignore_version_requirements,
            ignore_errors,
            poetry_extra_args,
            args.dry_run,
        )  # Pass ignore_errors flag


if __name__ == "__main__":
    main()
