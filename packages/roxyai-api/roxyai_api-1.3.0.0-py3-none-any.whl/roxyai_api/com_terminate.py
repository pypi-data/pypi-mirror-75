# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
from .com_definition import COM_TERMINATE
from .com_base import BaseCommand, STS_REPLY_ACK


class TerminateCommand(BaseCommand):
    code = COM_TERMINATE

    def __init__(self, connection=None):
        super().__init__(connection)
        # 要求データの設定
        self.data = b''

    def recv(self):
        reply_data = super().recv()
        # 応答データの妥当性チェック
        if len(reply_data) != 0:
            raise RuntimeError(f'mismatched terminate reply data')

    def __str__(self):
        string = f'Terminate(0x{self.code:02X}) '
        if self.status != STS_REPLY_ACK:
            string += f'-> {self.str_status()}'
        elif self.recv_time:
            string += f'-> ({self.get_process_time()} ms)'
        return string
