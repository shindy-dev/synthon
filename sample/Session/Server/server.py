import os
from synthon.network.server import ThreadingTCPServer, RequestHandler

class MyRequestHandler(RequestHandler):
    def on_handle(self, ts, ip, query):
        print(ts, ip, query)

    def handle_hello(self, query):
        self.send("こんにちは".encode(RequestHandler.ENCODING))


def serve_forever(host: str, port: int):
    ThreadingTCPServer((host, port), MyRequestHandler).serve_forever()
