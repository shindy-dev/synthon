"""
author: shindy-dev
created: 2020/10/26
github: https://github.com/shindy-dev
"""

import datetime
import socketserver
from network import _Transceiver


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
