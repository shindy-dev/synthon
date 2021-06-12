"""
author: shindy-dev
created: 2021/01/23
github: https://github.com/shindy-dev
"""

import os
import json
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
        cls.__set_value(
            cls.__MAX_QUERY_SIZE,
            "MAX_DATA_SIZE",
            v,
            516 * 1024 ** 2,
            10 * 1024 ** 3,
        )


class _Transceiver(metaclass=__TransceiverMeta):
    def recieve(self) -> bytes:
        self.request.settimeout(_Transceiver.TIMEOUT)
        return self.request.recv(_Transceiver.BUFF_SIZE)

    def _get_filesize(self) -> int:
        size = int(self.recieve().decode())
        self.send("size recieved".encode(_Transceiver.ENCODING))
        return size

    def recievefile(self) -> bytes:
        size = self._get_filesize()
        self.request.settimeout(_Transceiver.TIMEOUT)
        bytesData: bytearray = bytearray()
        while len(bytesData) < size:
            packet: bytes = self.request.recv(_Transceiver.BUFF_SIZE)
            bytesData.extend(packet)
        return bytes(bytesData)

    def recievefile_yield(self) -> bytes:
        size = self._get_filesize()
        self.request.settimeout(_Transceiver.TIMEOUT)
        bytesData: bytearray = bytearray()
        while len(bytesData) < size:
            packet: bytes = self.request.recv(_Transceiver.BUFF_SIZE)
            bytesData.extend(packet)
            yield packet, len(bytesData), size

    def recvQuery(self) -> Dict[str, Any]:
        return self._parseQuery(self.recieve())

    def send(self, bytesData: bytes):
        self.request.send(bytesData)

    def sendfile(self, path: str):
        self.send(str(os.path.getsize(path)).encode(_Transceiver.ENCODING))
        self.recieve().decode()
        with open(path, "rb") as file:
            self.request.sendfile(file)

    def sendQuery(self, query: Dict[str, Any]):
        self.send(self._createQuery(query))

    def _createQuery(self, query: Dict[str, Any]) -> bytes:
        return json.dumps(query).encode(_Transceiver.ENCODING)

    def _parseQuery(self, query: bytes) -> Dict[str, Any]:
        return dict(json.loads(query))
