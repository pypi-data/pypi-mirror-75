# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
import json

from .com_definition import COM_INITIALIZE
from .com_base import BaseCommand, STS_REPLY_ACK


class InitializeCommand(BaseCommand):

    code = COM_INITIALIZE
    send_json = ''

    def __init__(
        self,
        send_json: str = None,
        product: str = None,
        model_list: list = [],
        connection=None,
    ):
        super().__init__(connection)
        # 要求データの設定
        if send_json:
            self.product = None
            self.model_list = []
            self.send_json = send_json
        else:
            self.product = product
            self.model_list = model_list
            self.__encode_json()
        self.data = self.send_json.encode('utf-8')

    def append_model(self, model_name: str, group_name: str = None):
        """ モデルを追加する（オプションで画像グループ指定を行う）
        """
        if self.product is None:
            # jsonコードの未解釈の場合は一度解釈する
            dic = json.loads(self.send_json, encoding='utf-8')
            self.product = dic['Product']
            self.model_list = dic['ModelList']

        if group_name:
            self.model_list.append((str(model_name), str(group_name)))
        else:
            self.model_list.append(str(model_name))
        self.__encode_json()

    def __encode_json(self) -> str:
        model_list = []
        for model in self.model_list:
            if type(model) is list:
                if len(model) >= 2:
                    model = [str(model[0]), str(model[1])]
                else:
                    model = str(model[0])
            else:
                model = str(model)
            model_list.append(model)
        dic = {
            'Product': str(self.product),
            'ModelList': model_list
        }
        self.send_json = json.dumps(dic, ensure_ascii=False)

    def run(self):
        reply_data = super().run()
        # 応答データの妥当性チェック
        if len(reply_data) != 0:
            raise RuntimeError(f'mismatched initialize reply data')

    def __str__(self):
        string = (
            f'Initialize(0x{self.code:02X}) '
            f'SendJson: {self.send_json} '
            f'{len(self.send_json)} bytes '
        )
        if self.status != STS_REPLY_ACK:
            string += f'-> {self.str_status()}'
        elif self.recv_time:
            string += f'-> ({self.get_process_time()} ms)'
        return string
