#!/usr/bin/env python3


def preprocess_line(line: str) -> str:
    if line.startswith("#"):
        return ""
    return line.strip()
