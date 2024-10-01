from time import time, sleep
from hashlib import md5


class Generator:
    SLEEP_TIME = 1.0
    MAX_INT = 999999

    def __init__(self):
        self.now: int = int(time())
        self.auto_int: int = 0

    def get_int_id(self) -> int:
        _now: int = int(time())
        if self.now == _now:
            self.auto_int += 1
        else:
            self.now = _now
            self.auto_int = 0
        if self.auto_int > self.MAX_INT:
            sleep(self.SLEEP_TIME)
            return self.get_int_id()
        return self.now * (self.MAX_INT + 1) + self.auto_int

    def get_token(self) -> str:
        tmp_id: int = self.get_int_id()
        return md5(str(tmp_id).encode(encoding='utf-8')).hexdigest()

    def get_md5_str(self, input_str: str) -> str:
        return md5(input_str.encode(encoding='utf-8')).hexdigest()

    def get_verify_code(self) -> str:
        return self.get_token()[0:6]


gen = Generator()
