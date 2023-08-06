# (c) Roxy Corp. 2020-
# Roxy AI Inspect/Analyze-Server API
from .com_definition import COM_ECHO
from .com_base import BaseCommand, STS_REPLY_ACK


class EchoCommand(BaseCommand):
    code = COM_ECHO

    def __init__(self, data: bytes, connection=None):
        super().__init__(connection)
        # 要求データの設定
        self.data = data

    def recv(self):
        reply_data = super().recv()
        # 応答データの妥当性チェック
        if self.data != reply_data:
            raise RuntimeError(f'mismatched echo reply data')

    def __str__(self):
        string = (
            f'Echo(0x{self.code:02X}) '
            f'Data: {self.data[:min(len(self.data), 128)]} '
            f'{len(self.data):,} bytes '
        )
        if self.status != STS_REPLY_ACK:
            string += self.str_status()
        elif self.recv_time:
            string += f'-> ({self.get_process_time()} ms)'
        return string
