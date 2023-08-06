# (c) Roxy Corp. 2020-
# Roxy AI Analyze-Server API
import struct

from .com_definition import (
    COM_GET_PROBABILITIES,
    Probability,
)
from .com_base import (
    BaseCommand,
    HEADER_SIZE,
    STS_REPLY_ACK,
)


class GetProbabilitiesCommand(BaseCommand):

    code = COM_GET_PROBABILITIES
    PROB_SIZE = 13
    PROB_OFFSET = 14 - HEADER_SIZE

    # ログの詳細出力
    verbose = False

    def __init__(
        self,
        inspect_id: int,
        connection=None,
    ):
        super().__init__(connection)
        self.inspect_id = inspect_id
        self.data = struct.pack(f'< Q', inspect_id)

    def recv(self):
        reply_data = super().recv()

        if not reply_data:
            # エラー応答の場合
            self.prob_size = 0
            self.prob_list = []
            return

        try:
            prob_size, = struct.unpack(
                '< H',
                reply_data[:self.PROB_OFFSET]
            )
            prob_data = reply_data[self.PROB_OFFSET:]

            # 受信データの格納
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

    def __str__(self):
        string = (
            f'GetProbabilities(0x{self.code:02X}) '
            f'InspectID: {self.inspect_id}(=0x{self.inspect_id:#016X}) '
        )
        if self.status != STS_REPLY_ACK:
            string += f'-> {self.str_status()}'
        elif self.recv_time:
            string += (
                f'-> ProbabilityList: {self.prob_size} items '
                f'({self.get_process_time()} ms)'
            )
            if self.verbose:
                for prob in self.prob_list:
                    string += '\n    ' + str(prob)
        return string
