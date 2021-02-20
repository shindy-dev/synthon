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
    def on_handle(timestamp: datetime, ip: str, query: dict):
        pass

    def handle(self):
        ts = datetime.datetime.now()
        ip = self.client_address[0]
        print(f"[o]{ts}: {ip}")
        query: dict = {}
        try:
            query: dict = self.recvQuery()
            getattr(self, f"handle_{query['mode']}")(query)
        except Exception:
            print(f"invalid query: {query}")
        finally:
            self.request.close()
            print(f"[x]{ts}: {ip}")
            self.on_handle(ts, ip, query)


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
