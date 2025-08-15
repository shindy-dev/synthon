import sys

sys.path.append("../../")

from synthon.network.client import Client


class MyClient(Client):
    @Client.req
    def request_hello(self, **query):
        bytesData = self.recieve()
        return bytesData.decode(Client.ENCODING)

    @Client.req
    def request_sendfile(self, **query):
        self.recieve()
        self.sendfile(query["path"])
