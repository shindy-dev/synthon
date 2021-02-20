"""
author: shindy-dev
created: 2020/10/26
github: https://github.com/shindy-dev
"""

import datetime
import socketserver

try:
    from synthon.network._transceiver import _Transceiver
except ImportError:
    from _transceiver import _Transceiver


class ThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    # Overrides
    def serve_forever(self, poll_interval: float = 0.5):
        split: str = "=" * 15
        print(f"{split}   Open Server {split}")
        try:
            super().serve_forever(poll_interval)
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()
            self.server_close()
            print(f"{split} Closed Server {split}")


class RequestHandler(socketserver.BaseRequestHandler, _Transceiver):
    def handle(self):
        print(f"{datetime.datetime.now()}: {self.client_address[0]}")
        try:
            query: dict = self.recvQuery()
            getattr(self, f"handle_{query['mode']}")(query)
        except KeyError:
            print(f"invalid query: {query}")
        finally:
            self.request.close()


if __name__ == "__main__":
    import os
    from server import ThreadingTCPServer, RequestHandler

    class MyRequestHandler(RequestHandler):
        def handle_hello(self, query):
            self.send("こんにちは".encode(RequestHandler.ENCODING))

        def handle_sendfile(self, query):
            self.send(b"please")
            # bytesData = self.recievefile()
            # with open(f"【コピー】{os.path.basename(query['path'])}", mode="wb") as f:
            #     f.write(bytesData)

            for packet, current_size, size in self.recievefile_yield():
                # print(f"{current_size/1024**2}/{size/1024**2}")
                with open(f"【コピー】{os.path.basename(query['path'])}", mode="ab") as f:
                    f.write(packet)

    ThreadingTCPServer(("localhost", 22222), MyRequestHandler).serve_forever()
