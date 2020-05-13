from pprint import pprint
from io import IOBase
from urllib3 import PoolManager
from urllib.parse import urljoin
import logging

from .util import import_class
from .error import ConfigurationError

BACKEND_ALIAS = {
    'rucaptcha': 'captcha_solution.backend.rucaptcha:RucaptchaBackend',
    '2captcha': 'captcha_solution.backend.twocaptcha:TwocaptchaBackend',
    'anticaptcha': 'captcha_solution.backend.anticaptcha:AnticaptchaBackend',
}
logger = logging.getLogger('captcha_solution.base_backend')


class BaseBackend(object):
    software_id = ''
    default_network_timeout = 5
    base_url = None

    def __init__(self, api_key):
        self.api_key = api_key
        self.pool = PoolManager(cert_reqs='CERT_NONE')

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

    def request(self, method, url, headers=None, fields=None, body=None): 
        kwargs = {}
        if headers:
            kwargs['headers'] = headers
        if fields:
            kwargs['fields'] = fields
        if body:
            kwargs['body'] = body
        res = self.pool.request(
            'POST',
            url=urljoin(self.base_url, url),
            timeout=self.default_network_timeout,
            **kwargs,
        )
        logger.debug('res.php response: %s' % res.data)
        return res
