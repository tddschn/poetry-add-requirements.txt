#!/usr/bin/env python3


def preprocess_line(line: str) -> str:
    if line.startswith("#"):
        return ""
    if "#" in line:
        line, *_ = line.split("#")
    return line.strip()
