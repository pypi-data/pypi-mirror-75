# (c) Roxy Corp. 2020-
# Roxy AI Analyze-Server API
import struct

from .com_definition import COM_GET_IMAGE
from .com_base import (
    BaseCommand,
    HEADER_SIZE,
    STS_REPLY_ACK,
)


class GetImageCommand(BaseCommand):

    code = COM_GET_IMAGE
    PROB_OFFSET = 14 - HEADER_SIZE

    def __init__(
        self,
        inspect_id: int,
        connection=None,
    ):
        super().__init__(connection)
        self.inspect_id = inspect_id
        self.data = struct.pack(f'< Q', inspect_id)

    def recv(self):
        # 画像タイプまでを受信
        reply_data = super().recv(recv_size=1)

        if not reply_data:
            # エラー応答の場合
            self.data_format = None
            self.image_data = None
            return

        try:
            self.data_format, = struct.unpack('< B', reply_data)
        except Exception:
            raise RuntimeError(f'received invalid data')

        image_data = b''
        size = self.rest_size
        if size > 0:
            # 画像データの受信
            while len(image_data) < size:
                image_data += self.connection.sock.recv(size - len(image_data))
        self.image_data = image_data

    def __str__(self):
        string = (
            f'GetImage(0x{self.code:02X}) '
            f'InspectID: {self.inspect_id}(=0x{self.inspect_id:016X}) '
        )
        if self.status != STS_REPLY_ACK:
            string += f'-> {self.str_status()}'
        elif self.recv_time:
            string += (
                f'-> DataFromat: 0x{self.data_format:02X}, '
                f'ImageData: {len(self.image_data):,d} bytes '
                f'({self.get_process_time()} ms)'
            )
        return string
