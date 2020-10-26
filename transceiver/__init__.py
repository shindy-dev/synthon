"""
author: shindy-dev
created: 2020/10/26
github: https://github.com/shindy-dev
"""

__all__ = (
    "client",
    "server",
)

import json
from transceiver import client, server
from typing import Any, Dict


class __TransceiverMeta(type):
    def __init__(cls, *args, **kwargs):
        cls.__TIMEOUT: int = 60  # second
        cls.__ENCODING: str = "utf-8"
        cls.__BUFF_SIZE: int = 4096  # 4KiB
        cls.__MAX_QUERY_SIZE: int = 4096 * 512  # 2MiB
        cls.__MAX_DATA_SIZE: int = 5 * 1024 ** 3  # 5GiB

    @classmethod
    def __set_value(cls, priv: int, n: str, v: int, minv: int, maxv: int):
        if minv <= v and v <= maxv:
            priv = v
        else:
            raise Exception(f"{n} = {v} (Expected: {minv} <= {n} <= {maxv})")

    @property
    def TIMEOUT(cls) -> int:
        return cls.__TIMEOUT

    @TIMEOUT.setter
    def TIMEOUT(cls, v: int):
        cls.__set_value(cls.__TIMEOUT, "TIMEOUT", v, 0, 10 ** 2)

    @property
    def ENCODING(cls) -> str:
        return cls.__ENCODING

    @ENCODING.setter
    def ENCODING(cls, v: str):
        cls.__ENCODING = v

    @property
    def BUFF_SIZE(cls) -> int:
        return cls.__BUFF_SIZE

    @BUFF_SIZE.setter
    def BUFF_SIZE(cls, v: int):
        cls.__set_value(cls.__BUFF_SIZE, "BUFF_SIZE", v, 128, 1024 ** 2)

    @property
    def MAX_QUERY_SIZE(cls) -> int:
        return cls.__MAX_QUERY_SIZE

    @MAX_QUERY_SIZE.setter
    def MAX_QUERY_SIZE(cls, v: int):
        cls.__set_value(cls.__MAX_QUERY_SIZE, "MAX_QUERY_SIZE", v, 128, 8 * 1024 ** 2)

    @property
    def MAX_DATA_SIZE(cls) -> int:
        return cls.__MAX_DATA_SIZE

    @MAX_DATA_SIZE.setter
    def MAX_DATA_SIZE(cls, v: int):
        cls.__set_range_value(
            cls.__MAX_QUERY_SIZE,
            "MAX_DATA_SIZE",
            v,
            516 * 1024 ** 2,
            10 * 1024 ** 3,
        )


class _Transceiver(metaclass=__TransceiverMeta):
    def recieve(self, max_size: int = -1) -> bytes:
        if max_size < 0:
            max_size = _Transceiver.MAX_DATA_SIZE
        self.request.settimeout(_Transceiver.TIMEOUT)
        bytesData: bytearray = bytearray()
        while True:
            packet: bytes = self.request.recv(_Transceiver.BUFF_SIZE)
            bytesData.extend(packet)
            if len(packet) < _Transceiver.BUFF_SIZE or len(bytesData) > max_size:
                break
        return bytes(bytesData)

    def recvQuery(self) -> Dict[str, Any]:
        return self._parseQuery(self.recieve(_Transceiver.MAX_QUERY_SIZE))

    def send(self, bytesData: bytes):
        self.request.send(bytesData)

    def sendfile(self, path: str):
        with open(path, "rb") as file:
            self.request.sendfile(file)

    def sendQuery(self, query: Dict[str, Any]):
        self.send(self._createQuery(query))

    def _createQuery(self, query: Dict[str, Any]) -> bytes:
        return json.dumps(query).encode(_Transceiver.ENCODING)

    def _parseQuery(self, query: bytes) -> Dict[str, Any]:
        return dict(json.loads(query))