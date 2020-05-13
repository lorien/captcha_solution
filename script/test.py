import logging
import time
import json

from captcha_solution import CaptchaSolver, SolutionNotReady


with open('var/config.json') as inp:
        config = json.load(inp)


def setup_logging():
    for hdl in logging.getLogger().handlers:
        hdl.setFormatter(logging.Formatter(
            '%(name)s [%(levelname)s] %(message)s'
        ))


def main(**kwargs):
    setup_logging()
    engine = '2captcha'
    sol = CaptchaSolver(
        backend=engine,
        api_key=config['%s_key' % engine],
    )
    data = open('data/captcha.jpg', 'rb')
    #task_id = sol.submit(data)
    #while True:
    #    try:
    #        res = sol.check_result(task_id)
    #    except SolutionNotReady:
    #        print('Solution is not ready yet')
    #    else:
    #        print('Solution found: %s' % res)
    #        break
    #    time.sleep(2)
    print('Solution: %s' % sol.solve(data))
    #print('method: %s' % sol.backend.call_method('getSpendingStats'))
    print('Balance: %s' % sol.get_balance())
    #print('Solution: %s' % sol.solve({
    #    'lang': 'ru',
    #    'textcaptcha': 'как тебя зовут',
    #}))
