"""
author: shindy-dev
created: 2020/10/27
github: https://github.com/shindy-dev
"""

__all__ = (
    "dict2xml",
    "write_xml",
)

import copy
import os
import sys
from typing import Any, Dict, List
import xml.etree.ElementTree as ET
import xml.dom.minidom as md


def dict2xml(elements: Dict[str, Any], root_name: str = "root", set_type: bool = False):
    root = (
        ET.Element(root_name, type=type(elements).__name__)
        if set_type
        else ET.Element(root_name)
    )
    if isinstance(elements, list) or isinstance(elements, tuple):
        root = _v2xml(root, elements, dct=False, set_type=set_type)
    elif isinstance(elements, dict):
        root = _v2xml(root, elements, dct=True, set_type=set_type)
    else:
        raise TypeError("elements type is limited to dict, list, tuple.")
    return root


def write_xml(root: ET.Element, path: str, encoding: str = "utf-8"):
    with open(path, "w") as f:
        md.parseString(ET.tostring(root)).writexml(
            f, encoding=encoding, newl="\n", indent="", addindent="  "
        )


def _h(sub: ET.Element, v: Any, set_type: bool):
    if isinstance(v, list) or isinstance(v, tuple):
        _v2xml(sub, v, dct=False, set_type=set_type)
    elif isinstance(v, dict):
        _v2xml(sub, v, dct=True, set_type=set_type)
    else:
        sub.text = v.__str__()


def _v2xml(root: ET.Element, values: Any, dct: bool, set_type: bool):
    [
        _h(
            ET.SubElement(root, k, type=type(v).__name__)
            if set_type
            else ET.SubElement(root, k),
            v,
            set_type,
        )
        for k, v in values.items()
    ] if dct else [
        _h(
            ET.SubElement(root, "item", type=type(v).__name__)
            if set_type
            else ET.SubElement(root, "item"),
            v,
            set_type,
        )
        for v in values
    ]
    return root


if __name__ == "__main__":
    dct = {
        "hoge": 2,
        "huge": (2, 3, 4, "f", ["a", 0, 5, 5]),
        "buga": {"a": "1"},
        "rect": {
            "area": 30,
            "width": 5,
            "height": 6,
        },
    }
    root = dict2xml(dct, root_name="annotation", set_type=False)
    write_xml(root, "test.xml")