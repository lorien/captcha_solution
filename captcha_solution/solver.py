import time
import logging

from urllib3.exceptions import HTTPError

from .error import SolutionNotReady, OperationTimeout, NoSlotAvailable
from .base_backend import BaseBackend

logger = logging.getLogger('captcha_solution.solver')
DEFAULT_SUBMIT_TASK_TIMEOUT = 30
DEFAULT_CHECK_RESULT_TIMEOUT = 120
DEFAULT_NETWORK_TIMEOUT = 5


class CaptchaSolver(object):
    def __init__(
            self,
            backend,
            api_key=None,
            submit_task_timeout=DEFAULT_SUBMIT_TASK_TIMEOUT,
            check_result_timeout=DEFAULT_CHECK_RESULT_TIMEOUT,
        ):
        self.api_key = api_key
        if isinstance(backend, BaseBackend):
            self.backend = backend
        else:
            self.backend = BaseBackend.get_backend_class(backend)(
                api_key=self.api_key
            )
        self.submit_task_timeout = submit_task_timeout
        self.check_result_timeout = check_result_timeout

    def submit(self, data=None):
        start = time.time() 
        while True:
            if time.time() - start > self.submit_task_timeout:
                raise OperationTimeout(
                    'Could not submit task in %d seconds'
                    % self.submit_task_timeout
                )
            try:
                return self.backend.submit(data=data)
            except (NoSlotAvailable, HTTPError, OSError) as ex:
                logger.debug('Retrying to submit task. Error is %s' % ex)
            time.sleep(3)

    def check_result(self, task_id):
        start = time.time() 
        while True:
            if time.time() - start > self.check_result_timeout:
                raise OperationTimeout(
                    'Could not get task result in %d seconds'
                    % self.check_result_timeout
                )
            try:
                return self.backend.check_result(task_id)
            except (SolutionNotReady, HTTPError, OSError) as ex:
                logger.debug('Retrying to get task result. Error is %s' % ex)
            time.sleep(3)

    def solve(self, data=None):
        task_id = self.submit(data)['task_id']
        while True:
            try:
                res = self.check_result(task_id)
            except SolutionNotReady as ex:
                logger.debug('Solution is not ready for task %s' % task_id)
            else:
                return res
            time.sleep(2)

    def get_balance(self):
        return self.backend.get_balance()
