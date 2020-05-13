from io import IOBase
from urllib3 import PoolManager

from .util import import_class
from .error import ConfigurationError

BACKEND_ALIAS = {
    'rucaptcha': 'captcha_solution.backend.rucaptcha:RucaptchaBackend',
}


class BaseBackend(object):
    default_network_timeout = 5

    def __init__(self, api_key):
        self.api_key = api_key
        self.pool = PoolManager()

    @classmethod
    def get_backend_class(cls, name):
        if name in BACKEND_ALIAS:
            name = BACKEND_ALIAS[name]
        return import_class(name)

    def submit(self, data=None):
        raise NotImplementedError

    def check_solution(self, task_id):
        raise NotImplementedError

    def get_balance(self):
        raise NotImplementedError

    def normalize_input_data(self, data):
        if isinstance(data, IOBase):
            data = data.read()
        if isinstance(data, (bytes, dict)):
            return data
        else:
            raise ConfigurationError(
                'Submit data must one of these types: file handler, bytes, dict'
            )
