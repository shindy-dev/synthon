"""
author: shindy-dev
created: 2020/10/03
github: https://github.com/shindy-dev
"""
__all__ = (
    "wc_l",
    "wc_m",
    "wc_c",
)
import os
from typing import List, Dict


def _abs(path: str):
    return path if os.path.isabs(path) else os.path.abspath(path)


def _get_paths(path: str, exts: List[str], excludes: List[str]) -> List[str]:
    if isinstance(excludes, str):
        excludes = [excludes]
    if isinstance(exts, str):
        exts = [exts]
    path = _abs(path)
    if os.path.isfile(path):
        return [path]
    exts = [ext if ext.startswith(".") else "." + ext for ext in exts]
    excludes = [_abs(e) for e in excludes]
    paths: List[str] = []
    for root, dirs, files in os.walk(os.path.abspath(path)):
        flg: bool = False
        for exclude in excludes:
            if os.path.abspath(root).startswith(exclude):
                flg = True
        if not flg:
            for file in files:
                if not exts or os.path.splitext(file)[-1] in exts:
                    paths.append(os.path.join(root, file))
    return paths


def wc_l(path: str, exts: List[str] = [], excludes: List[str] = []) -> int:
    """
    Get the number of lines from files like wc -l command
    """
    paths = _get_paths(path, exts, excludes)
    print(paths)
    sum_lines = 0
    for path in paths:
        with open(path, "rb") as f:
            sum_lines += len(f.readlines())
    return sum_lines


def wc_m(path: str, exts: List[str] = [], excludes: List[str] = []) -> int:
    """
    Get the number of multi-byte from files like wc -m command
    """
    paths = _get_paths(path, exts, excludes)
    sum_multibytes = 0
    print(paths)
    for path in paths:
        with open(path, "rb") as f:
            sum_multibytes += sum(
                [len(line.decode().strip("\n")) for line in f.readlines()]
            )
    return sum_multibytes


def wc_c(path: str, exts: List[str] = [], excludes: List[str] = []) -> int:
    """
    Get the number of bytes from files like wc -c command
    """
    paths = _get_paths(path, exts, excludes)
    sum_bytes = 0
    print(paths)
    for path in paths:
        with open(path, "rb") as f:
            sum_bytes += sum(
                [len(line.decode().strip("\n").encode()) for line in f.readlines()]
            )
    return sum_bytes


if __name__ == "__main__":
    print(wc_m("ls.py"))