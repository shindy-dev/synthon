"""
author: shindy-dev
created: 2020/10/26
github: https://github.com/shindy-dev
"""

import socket

try:
    from synthon.network._transceiver import _Transceiver
except ImportError:
    from _transceiver import _Transceiver


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


if __name__ == "__main__":

    from client import Client

    class MyClient(Client):
        @Client.req
        def request_hello(self, query):
            bytesData = self.recieve()
            return bytesData.decode(Client.ENCODING)

    client = MyClient(("localhost", 22222))
    print(client.request_hello({"mode": "hello"}))