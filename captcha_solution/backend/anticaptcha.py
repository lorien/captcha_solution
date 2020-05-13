from pprint import pprint
import json
import logging
from base64 import b64encode

from ..error import (
    RemoteServiceError, UnexpectedServiceResponse,
    ZeroBalance, SolutionNotReady, NoSlotAvailable
)
from ..base_backend import BaseBackend
from ..error import ConfigurationError

logger = logging.getLogger('captcha_solution.backend.anticaptcha')


class AnticaptchaBackend(BaseBackend):
    base_url = 'https://api.anti-captcha.com'

    ### Submit Task

    def submit(self, data=None):
        data = self.normalize_input_data(data)
        extra_fields = {}
        if isinstance(data, bytes):
            extra_fields = {
                'task': {
                    'type': 'ImageToTextTask',
                    'body': b64encode(data).decode(),
                },
            }
        else:
            extra_fields = data
        res = self.request(
            'POST', '/createTask',
            **self.prepare_request(fields=extra_fields)
        )
        return self.parse_submit_task_response(res.status, res.data)

    def parse_submit_task_response(self, status, data):
        if status != 200:
            raise UnexpectedServiceResponse(
                'Remote service return result with code %s' % status
            )
        data = json.loads(data.decode('utf-8'))
        if data['errorId'] == 0:
            return {
                'task_id': data['taskId'],
                'raw': data,
            }
        else:
            error = data['errorDescription']
            raise RemoteServiceError(error, error)

    ### Check Result

    def check_result(self, task_id):
        res = self.request(
            'GET', '/getTaskResult',
            **self.prepare_request(fields={'taskId': task_id}),
        )
        return self.parse_check_result_response(res.status, res.data, task_id)

    def parse_check_result_response(self, status, data, task_id):
        if status != 200:
            raise UnexpectedServiceResponse(
                'Remote service return result with code %s' % status
            )
        data = json.loads(data.decode('utf-8'))
        if data['errorId'] == 0:
            if data['status'] == 'processing':
                raise SolutionNotReady('task is processing', 'processing')
            else:
                return {
                    'solution': data['solution'],
                    'raw': data,
                }
        else:
            ecode = data['errorCode']
            edesc = data['errorDescription']
            if error == 'ERROR_ZERO_BALANCE':
                raise ZeroBalance(ecode, edesc)
            elif error == 'ERROR_NO_SLOT_AVAILABLE':
                raise NoSlotAvailable(ecode, edesc)
            else:
                raise RemoteServiceError(ecode, edesc)

    ### Call Method

    def call_method(self, method, fields=None):
        res = self.request(
            'GET', method,
            **self.prepare_request(fields),
        )
        return self.parse_call_method_response(res.status, res.data)

    def parse_call_method_response(self, status, data):
        if status != 200:
            raise UnexpectedServiceResponse(
                'Remote service return result with code %s' % status
            )
        data = json.loads(data.decode('utf-8'))
        if data.get('errorId'):
            ecode = data['errorCode']
            edesc = data['errorDescription']
            raise RemoteServiceError(ecode, edesc)
        else:
            return data

    ### Get Balance

    def get_balance(self):
        return self.call_method('getBalance')['balance']

    ### Utilities
    def prepare_request(self, fields=None):
        req_fields = {
            'clientKey': self.api_key,
            'softId': self.software_id,
        }
        req_headers = {
            'Content-Type': 'application/json',
        }
        check_keys = ['clientKey']
        if fields:
            if any(x in fields for x in check_keys):
                raise ConfigurationError(
                    'It is not allowed to change these keys: {}'.format(
                        ', '.join(check_keys)
                    )
                )
            req_fields.update(fields)
        req_body = json.dumps(req_fields)
        return {
            'headers': req_headers,
            'fields': None,
            'body': req_body,
        }


