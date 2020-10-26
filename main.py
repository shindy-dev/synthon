import os
import ls
from stopwatch import stopwatch


@stopwatch
def a():
    return "hoge"


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    print(ls.ls_all(path))