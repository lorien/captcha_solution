## Captcha Solution Python Package

Captcha Solution package is a simple interface to multiple captcha solving services.

## Image Captcha Example

```python
from captcha_solution import CaptchaSolver

solver = CaptchaSolver('anticaptcha', api_key='YOUR-API-KEY')
with open('captcha.png', 'rb') as inp:
    print(solver.solve(inp))
```

## Supported Captcha Services

* [2captcha.com](https://2captcha.com?from=3019071) - `2captcha`
* [rucaptcha.com](https://rucaptcha.com?from=3019071) - `rucaptcha`
* [anti-captcha.com](http://getcaptchasolution.com/ijykrofoxz) - `anticaptcha`
