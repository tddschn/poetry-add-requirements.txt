#!/usr/bin/env python3

def preprocess_line(line: str) -> str:
    return line.removeprefix('#').strip()