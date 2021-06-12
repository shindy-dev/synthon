"""
author: shindy-dev
created: 2020/10/25
github: https://github.com/shindy-dev
"""
__all__ = ("stopwatch",)

import datetime
import time
import os
from dataclasses import dataclass, fields
from typing import Any, ClassVar, Dict, List


def _fmt(*args: List[Any], show: bool = False):
    return ",".join(["{:32}".format(arg) for arg in args] if show else args)


# stopwatch_elements
@dataclass(frozen=True)
class _sw_e:
    func_name: str
    proc_time: float
    exec_datetime: str

    def log(self, show: bool = False) -> str:
        return _fmt(*[getattr(self, f.name) for f in fields(self)], show=show)

    @classmethod
    def log_head(cls, show: bool = False) -> str:
        return _fmt(*[f.name.upper() for f in fields(cls)], show=show)

    @classmethod
    def log_split(cls) -> str:
        return ("#-" * int(len(cls.log_head(show=True)) / 2)).rstrip("-")

    @classmethod
    def _wfmt(cls, s: str, end: str = "\n", enc: str = "utf-8"):
        return f"{s}{end}".encode(enc)


class stopwatch:
    """
    This stopwatch class is a class that measures the processing time of a function.
    - showing the result using "stopwatch.show" function.
    - saving the result using "stopwatch.write" function.
    """

    # history
    _hist: List[_sw_e] = []

    def __new__(cls, func: Any) -> Any:
        if not callable(func):
            raise TypeError(f"'{type(func)}' object is not callable")

        def w(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            s: float = time.time()
            r: Any = func(*args, **kwargs)
            e: _sw_e = _sw_e(
                func.__qualname__,
                f"{time.time() - s:.8f}",
                datetime.datetime.now().strftime("%F %H:%M:%S.%f"),
            )
            cls._hist.append(e)
            return r

        return w

    @classmethod
    def show(cls):
        print(
            *(
                [_sw_e.log_split()]
                + [
                    _sw_e.log_head(show=True),
                    *[e.log(show=True) for e in cls._hist],
                ]
                + [_sw_e.log_split()]
            ),
            sep="\n",
        )

    @classmethod
    def write(cls, path: str, clear: bool = False, encoding: str = "utf-8"):
        exists = os.path.exists(path)
        with open(path, "wb" if clear else "ab") as f:
            if clear or not exists:
                f.write(_sw_e._wfmt(_sw_e.log_head(), enc=encoding))
            f.writelines([_sw_e._wfmt(e.log(), enc=encoding) for e in cls._hist])


# example
if __name__ == "__main__":

    class SampleClass:
        @classmethod
        @stopwatch
        def sample_method(cls):
            return [i for i in range(10 ** 6)]

    sample = SampleClass()
    sample.sample_method()

    # main
    stopwatch.show()
    stopwatch.write("sample.log")
