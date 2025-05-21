"""
author: shindy-dev
created: 2020/10/03
github: https://github.com/shindy-dev
"""
__all__ = (
    "wc_c",
    "wc_l",
    "wc_m",
    "wc_w",
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


# バイト数取得
def wc_c(path: str, exts: List[str] = [], excludes: List[str] = []) -> int:
    """
    Get the number of bytes from files like wc -c command
    """
    paths = _get_paths(path, exts, excludes)
    sum_bytes = 0
    for path in paths:
        with open(path, "rb") as f:
            sum_bytes += len(f.read())
                
    return sum_bytes


# 行数取得
def wc_l(path: str, exts: List[str] = [], excludes: List[str] = []) -> int:
    """
    Get the number of lines from files like wc -l command
    """
    paths = _get_paths(path, exts, excludes)
    sum_lines = 0
    for path in paths:
        with open(path, "rb") as f:
            sum_lines += len(f.readlines())
    return sum_lines


# 文字数（マルチバイト）取得
def wc_m(path: str, exts: List[str] = [], excludes: List[str] = []) -> int:
    """
    Get the number of multi-byte from files like wc -m command
    """
    paths = _get_paths(path, exts, excludes)
    sum_multibytes = 0
    for path in paths:
        with open(path, "rb") as f:
            sum_multibytes += sum(
                [len(line.decode().strip("\n")) for line in f.readlines()]
            )
    return sum_multibytes


# 単語数取得
def wc_w(path: str, exts: List[str] = [], excludes: List[str] = []) -> int:
    """
    Get the number of words from files like wc -w command
    """
    paths = _get_paths(path, exts, excludes)
    sum_words = 0
    for path in paths:
        with open(path, "rb") as f:
            sum_words += sum(
                [len(line.decode().strip("\n").split()) for line in f.readlines()]
            )
    return sum_words


if __name__ == "__main__":
    import wc

    path = os.path.join(os.path.dirname(__file__), "ls.py")
    print(f"word: {wc.wc_w(path)}")
    print(f"bytes-charactar: {wc.wc_m(path)}")
    print(f"multibytes-charactar: {wc.wc_c(path)}")
    print(f"lines: {wc.wc_l(path)}")
