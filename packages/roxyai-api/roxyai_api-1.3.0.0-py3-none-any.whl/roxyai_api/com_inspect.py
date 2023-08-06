# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
from typing import List
import struct
import numpy as np
from datetime import datetime


from .com_definition import (
    COM_INSPECT,
    Probability,
)
from .com_base import (
    BaseCommand,
    HEADER_SIZE,
    STS_REQUEST,
    STS_REPLY_ACK
)


# コマンド定数定義
RESULT_OK = 0x01
RESULT_NOK = 0x02
RESULT_UNK = 0x03
RESULT_FAILED = 0xFF

IMG_FORMAT_RAW = 0x01
IMG_FORMAT_JPEG = 0x02
IMG_FORMAT_PNG = 0x03


class InspectCommand(BaseCommand):

    code = COM_INSPECT
    PROB_SIZE = 13
    PROB_OFFSET = 19 - HEADER_SIZE

    RESULTS = (
        RESULT_OK,
        RESULT_NOK,
        RESULT_UNK,
        RESULT_FAILED,
    )

    # Requestパラメータ
    inspect_id = None
    model_id = None
    data_format = None
    image_data = b''
    # Replayパラメータ
    status = STS_REQUEST
    result = None
    prob_size = 0
    prob_list: List[Probability] = []

    # ログの詳細出力
    verbose = False

    def __init__(
        self,
        inspect_id: int,
        model_id: int,
        data_format: int,
        image_data: bytes = b'',
        connection=None,
    ):
        super().__init__(connection)
        # 要求データの設定
        if inspect_id is None:
            self.inspect_id = self.get_datetime_id()
        else:
            self.inspect_id = inspect_id
        self.model_id = model_id
        self.data_format = data_format
        self.image_data = b''
        self.extension = image_data
        self.encode_data()

    def encode_data(self):
        send_params = (
            self.inspect_id,
            self.model_id,
            self.data_format,
            self.image_data,
        )
        self.data = struct.pack(f'< Q B B {len(self.image_data)}s', *send_params)

    def set_rgb_raw_image(self, data: np.ndarray):
        # 構造情報の設定
        shape = data.shape
        if len(shape) == 2:
            # グレースケールの場合は色数情報を追加
            shape = (*shape, 1)
        self.image_data = struct.pack(f'< H H B', *shape)
        self.extension = data.tobytes()
        self.data_format = IMG_FORMAT_RAW
        self.encode_data()

    def set_jpeg_image(self, data: bytes):
        self.image_data = b''
        self.extension = data
        self.data_format = IMG_FORMAT_JPEG
        self.encode_data()

    def set_png_image(self, data: bytes):
        self.image_data = b''
        self.extension = data
        self.data_format = IMG_FORMAT_PNG
        self.encode_data()

    def send(self):
        super().send(extension=self.extension)

    def recv(self):
        reply_data = super().recv()
        self.check_reply(reply_data)

    def check_reply(self, reply):
        if not reply:
            self.result = None
            self.prob_size = 0
            self.prob_list = []
            return

        inspect_id, result, prob_size = struct.unpack(
            '< Q B H',
            reply[:self.PROB_OFFSET]
        )
        prob_data = reply[self.PROB_OFFSET:]

        # 受信データのチェック
        if self.inspect_id != inspect_id:
            raise RuntimeError(
                f'mismatched inspect_id '
                f'recv:{inspect_id}(=0x{inspect_id:#016X}) != '
                f'send:{self.inspect_id}(=0x{self.inspect_id:#016X})')

        # 受信データの格納
        try:
            self.result = result
            self.prob_size = prob_size
            self.prob_list = []
            for offset in range(0, prob_size * self.PROB_SIZE, self.PROB_SIZE):
                x1, y1, x2, y2, typ, prob = struct.unpack(
                    '< H H H H B f',
                    prob_data[offset:offset + self.PROB_SIZE]
                )
                prob = Probability(x1, y1, x2, y2, typ, prob)
                self.prob_list.append(prob)
        except Exception:
            raise RuntimeError(f'received invalid data')

    @classmethod
    def get_datetime_id(cls):
        dt = datetime.now()
        dtid = int(dt.strftime('%Y%m%d%H%M%S%f')) // 1000
        return dtid

    def __str__(self):
        image_size = len(self.image_data) + len(self.extension)
        string = (
            f'Inspector(0x{self.code:02X}) '
            f'InspectID: {self.inspect_id}(=0x{self.inspect_id:#016X}, '
            f'ModelID: {self.model_id}, '
            f'DataFormat: 0x{self.data_format:02X}, '
            f'ImageData: {image_size:,d} bytes '
        )
        if self.status != STS_REPLY_ACK:
            string += f'-> {self.str_status()}'
        elif self.result:
            string += (
                f'-> Result: 0x{self.result:02X}, '
                f'ProbabilitySize: {self.prob_size}, '
                f'ProbabilityList: {self.prob_size} items '
            )
            if self.recv_time:
                string += f'({self.get_process_time()} ms)'
            if self.verbose:
                for prob in self.prob_list:
                    string += '\n    ' + str(prob)
        return string
