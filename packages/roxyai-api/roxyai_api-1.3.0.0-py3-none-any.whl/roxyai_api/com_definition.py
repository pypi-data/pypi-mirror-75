# (c) Roxy Corp. 2020-, CONFIDENTIAL
# Roxy AI Inspect-Server communication definition

# フレームのヘッダ定義
SIGN_CODE = 0x6941
HEADER_SIZE = 8

# ステータス定義
STS_REQUEST = 0x00
STS_REPLY_ACK = 0x01
ERR_INVALID_DATA_SIZE = 0x0D
ERR_UNKNOWN_EXCEPTION = 0x0E
ERR_INVALID_COMMAND = 0x0F
ERR_NOT_FOUND_PRODUCT = 0x11
ERR_NOT_FOUND_MODEL = 0x12
ERR_DENIED_PRODUCT = 0x13
ERR_FAILED_LOAD_CONFIG = 0x14
ERR_FAILED_INITIALIZE = 0x15
ERR_FAILED_LOGGING = 0x16
ERR_INVALID_MODEL_ID = 0x21
ERR_INVALID_IMG_FORMAT = 0x22
ERR_INVALID_IMG_DATA = 0x23
ERR_INVALID_JSON_DATA = 0x24
ERR_UNINITIALIZED = 0x25
ERR_OVERLAP_INSPECT_ID = 0x26
ERR_FAILED_INSPECT = 0x27
ERR_NOT_FOUND_PROB = 0x28
ERR_NOT_FOUND_IMAGE = 0x29

STATUS_LIST = {
    STS_REQUEST: 'Request',
    STS_REPLY_ACK: 'ACK',
    ERR_INVALID_DATA_SIZE: 'ERR: Invalid command data size',
    ERR_UNKNOWN_EXCEPTION: 'ERR: Unknown exception',
    ERR_INVALID_COMMAND: 'ERR: Unknown command',
    ERR_NOT_FOUND_PRODUCT: 'ERR: Cannot find product folder',
    ERR_NOT_FOUND_MODEL: 'ERR: Cannot find model data',
    ERR_DENIED_PRODUCT: 'ERR: Denied open additional product',
    ERR_FAILED_LOAD_CONFIG: 'ERR: Loading config file failed',
    ERR_FAILED_INITIALIZE: 'ERR: Model initialization failed',
    ERR_FAILED_LOGGING: 'ERR: Output inspection log failed',
    ERR_INVALID_MODEL_ID: 'ERR: Invalid model id',
    ERR_INVALID_IMG_FORMAT: 'ERR: Invalid image format id',
    ERR_INVALID_IMG_DATA: 'ERR: Invalid image data',
    ERR_INVALID_JSON_DATA: 'ERR: Invalid JSON data',
    ERR_UNINITIALIZED: 'ERR: Uninitialized',
    ERR_OVERLAP_INSPECT_ID: 'ERR: Overlapped inspect id',
    ERR_FAILED_INSPECT: 'ERR: Inspection failed',
    ERR_NOT_FOUND_PROB: 'ERR: Cannot find probabilities list',
    ERR_NOT_FOUND_IMAGE: 'ERR: Cannot find image data',
}

# コマンドの定義
COM_ECHO = 0x10
COM_INITIALIZE = 0x11
COM_TERMINATE = 0x12
COM_INSPECT = 0x13
COM_GET_PROBABILITIES = 0x1A
COM_GET_IMAGE = 0x1B

COM_LIST = {
    COM_ECHO: 'Echo',
    COM_INITIALIZE: 'Initialize',
    COM_TERMINATE: 'Terminate',
    COM_INSPECT: 'Inspect',
    COM_GET_PROBABILITIES: 'GetProbabilities',
    COM_GET_IMAGE: 'GetImage',
}


def get_status(status):
    return STATUS_LIST.get(status, 'Unknown Status')


def get_command(command):
    return COM_LIST.get(command, 'Unknown Command Code')


class Probability():
    TYPE_STR = {
        0x01: 'OK',
        0x02: 'NOK',
        0x03: 'UNK',
        0xFF: 'Failed'
    }

    def __init__(self, x1, y1, x2, y2, typ, prob):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.typ = typ
        self.prob = prob

    def __str__(self):
        return (
            f'{self.TYPE_STR.get(self.typ):3s} '
            f'({self.x1:4d}, {self.y1:4d})-({self.x2:4d}, {self.y2:4d}) '
            f'{self.prob:6f}'
        )
