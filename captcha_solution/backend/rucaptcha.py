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
    base_url = 'https://rucaptcha.com'

    ### Submit Task

    def submit(self, data=None):
        data = self.normalize_input_data(data)
        extra_fields = {}
        if isinstance(data, bytes):
            extra_fields = {
                'method': 'post',
                'file': ('captcha.jpg', data),
            }
        else:
            extra_fields = data
        res = self.request(
            'POST', '/in.php',
            **self.prepare_request(extra_fields)
        )
        res_data = json.loads(res.data.decode('utf-8'))
        return self.parse_submit_task_response(res.status, res.data)

    def parse_submit_task_response(self, status, data):
        if status != 200:
            raise UnexpectedServiceResponse(
                'Remote service return result with code %s' % status
            )
        data = json.loads(data.decode('utf-8'))
        if data['status'] == 1:
            return {
                'task_id': data['request'],
                'raw': data,
            }
        else:
            error = data['request']
            if error == 'ERROR_ZERO_BALANCE':
                raise ZeroBalance(error, error)
            elif error == 'ERROR_NO_SLOT_AVAILABLE':
                raise NoSlotAvailable(error, error)
            else:
                raise RemoteServiceError(error, error)

    ### Check Result

    def check_result(self, task_id):
        res = self.request(
            'GET', '/res.php',
            **self.prepare_request({
                'action': 'get',
                'id': task_id,
            }),
        )
        return self.parse_check_result_response(res.status, res.data, task_id)

    def parse_check_result_response(self, status, data, task_id):
        if status != 200:
            raise UnexpectedServiceResponse(
                'Remote service return result with code %s' % status
            )
        data = json.loads(data.decode('utf-8'))
        if data['status'] == 1:
            return {
                'solution': data['request'],
                'raw': data,
            }
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

    ### Get Balance

    def get_balance(self):
        res = self.request(
            'GET', '/res.php',
            **self.prepare_request({
                'action': 'getbalance',
            }),
        )
        return self.parse_get_balance_response(res.status, res.data)

    def parse_get_balance_response(self, status, data):
        if status != 200:
            raise UnexpectedServiceResponse(
                'Remote service return result with code %s' % status
            )
        data = json.loads(data.decode('utf-8'))
        if data['status'] == 1:
            return {
                'balance': float(data['request']),
                'raw': data,
            }
        else:
            error = data['request']
            raise RemoteServiceError(error, error)

    ### Utilities
    def prepare_request(self, fields=None):
        req_fields = {
            'key': self.api_key,
            'json': 1,
            'soft_id': self.software_id,
        }
        req_headers = {}
        check_keys = ['key', 'json']
        if any(x in fields for x in check_keys):
            raise ConfigurationError(
                'It is not allowed to change these keys: {}'.format(
                    ', '.join(check_keys)
                )
            )
        req_fields.update(fields)
        return {
            'headers': None,
            'fields': req_fields,
            'body': None,
        }
