# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
import socket
from threading import Lock
from time import sleep

from .com_base import BaseCommand
from .com_echo import EchoCommand

import logging.config
log = logging.getLogger(__name__)


class Connection():

    # # クラス変数
    # # 接続中のインスタンスを管理
    # current = None

    # サーバのデフォルト定義
    HOST = '127.0.0.1'
    PORT = 6945

    # 接続管理定数
    RETRY_INTERVAL = 0.2    # sec

    def __init__(self, host: str = HOST, port: int = PORT, retry: int = None):
        """ Inspect-Serverへの接続管理を行うクラス
            Args:
                host: str     接続先ホストIPv4アドレス（Option）
                port: int     接続先ホストTCPポート（Option）
        """
        self.host = host
        self.port = port
        self.lock = Lock()
        self.sock = None
        self.retry = retry

    def __enter__(self):
        """ 接続開始 for with構文
            Args:
        """
        self.open(retry=self.retry)

    def __exit__(self, exc_type, exc_value, traceback):
        """ 接続完了 for with構文
        """
        self.close()

    def open(self, retry: int = None):
        """ 接続開始
            Args:
                retry   :   サーバがビジーの場合に接続をリトライする回数(Option)
        """
        if not self.sock:
            log.debug(f'wait lock {id(self)}')
            self.lock.acquire()
            log.debug(f'acuire lock {id(self)}')

            count = 0
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while True:
                try:
                    self.sock.connect((self.host, self.port))
                    # 接続確認用のECHOコマンド
                    EchoCommand(b'', connection=self).run
                except ConnectionError as e:
                    self.sock.close()
                    count += 1
                    if (retry is None) or (count < retry):
                        log.info(f'connection retry {count}/{retry} by {type(e)}')
                        sleep(self.RETRY_INTERVAL)
                        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        continue
                    else:
                        log.warn(f'connection refused by server by {type(e)}')
                        self.sock = None
                        break
                else:
                    BaseCommand.connection = self
                    log.info(f'\n---- connect {self}')
                    break

    def close(self):
        """ 接続完了
        """
        if self.sock:
            info = str(self)
            self.sock.close()
            log.info(f'\n---- close {info}')

            self.sock = None
            BaseCommand.connection = None

            log.debug(f'release lock {id(self)}')
            self.lock.release()

    def __str__(self):
        if self.sock:
            sockname = self.sock.getsockname()
            peername = self.sock.getpeername()
            return f'connection: {sockname[0]}:{sockname[1]} -> {peername[0]}:{peername[1]}'
        else:
            return f'connection: unconnected'
