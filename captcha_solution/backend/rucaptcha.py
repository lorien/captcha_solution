import json
import json
import logging

from ..error import (
    RemoteServiceError, UnexpectedServiceResponse,
    ZeroBalance, SolutionNotReady, NoSlotAvailable
)
from ..base_backend import BaseBackend
from ..error import ConfigurationError

logger = logging.getLogger('captcha_solution.backend.rucaptcha')


class RucaptchaBackend(BaseBackend):
    software_id = '' 

    def submit(self, data=None):
        data = self.normalize_input_data(data)
        fields = {
            'key': self.api_key,
            'json': 1,
            'soft_id': self.software_id,
        }
        if isinstance(data, bytes):
            fields.update({
                'method': 'post',
                'file': ('captcha.jpg', data),
            })
        else:
            check_keys = ['key', 'json']
            if any(x in data for x in check_keys):
                raise ConfigurationError(
                    'It is not allowed to change these keys: {}'.format(
                        ', '.join(check_keys)
                    )
                )
            fields.update(data)
        res = self.pool.request(
            'POST',
            url='https://rucaptcha.com/in.php',
            fields=fields,
            timeout=self.default_network_timeout
        )
        logger.debug('in.php response: %s' % res.data)
        res_data = json.loads(res.data.decode('utf-8'))
        return int(res_data['request'])

    def check_result(self, task_id):
        res = self.pool.request(
            'GET',
            url='https://rucaptcha.com/res.php',
            fields={
                'key': self.api_key,
                'action': 'get',
                'id': task_id,
                'json': 1,
            },
            timeout=self.default_network_timeout
        )
        logger.debug('res.php response: %s' % res.data)
        return self.parse_check_result_response(res.status, res.data, task_id)

    def parse_check_result_response(self, status, data, task_id):
        if status != 200:
            raise UnexpectedServiceResponse(
                'Remote service return result with code %s' % status
            )
        data = json.loads(data.decode('utf-8'))
        if data['status'] == 1:
            return data['request']
        else:
            error = data['request']
            if error == 'CAPCHA_NOT_READY':
                raise SolutionNotReady(error, error)
            elif error == 'ERROR_ZERO_BALANCE':
                raise ZeroBalance(error, error)
            elif error == 'ERROR_NO_SLOT_AVAILABLE':
                raise NoSlotAvailable(error, error)
            else:
                raise RemoteServiceError(error, error)

    def parse_get_balance_response(self, status, data):
        if status != 200:
            raise UnexpectedServiceResponse(
                'Remote service return result with code %s' % status
            )
        data = json.loads(data.decode('utf-8'))
        if data['status'] == 1:
            return float(data['request'])
        else:
            error = data['request']
            raise RemoteServiceError(error, error)

    def get_balance(self):
        res = self.pool.request(
            'GET',
            url='https://rucaptcha.com/res.php',
            fields={
                'key': self.api_key,
                'action': 'getbalance',
                'json': 1,
            },
            timeout=self.default_network_timeout
        )
        logger.debug('res.php response: %s' % res.data)
        return self.parse_get_balance_response(res.status, res.data)
