"""
author: shindy-dev
created: 2020/10/26
github: https://github.com/shindy-dev
"""

import socket
from network import _Transceiver


class Client(_Transceiver):
    def __init__(self, fmt: tuple):
        self.fmt = fmt
        self.request: socket.socket = None

    @classmethod
    def req(cls, req_func):
        def inner(self, *args, **kwargs):

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as request:
                self.request = request
                self.request.connect(self.fmt)
                self.sendQuery(args[0])
                ret = req_func(self, *args, **kwargs)
            self.request.close()
            self.request = None

            return ret

        return inner
