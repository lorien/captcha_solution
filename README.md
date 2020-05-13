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

* 2captcha.com - `2captcha`
* rucaptcha.com - `rucaptcha`
* anticaptcha.com - `anticaptcha`
