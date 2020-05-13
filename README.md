## Captcha Solution Python Package

Captcha Solution package is a simple interface to multiple captcha solving services.

## Image Captcha Example

The simplest case is to solve captcha image stored into file.
Pass the file handler to the `solve` method. The solution will
be stored into "solution" key of returned result. In "raw" key
there is a full original response that returned captcha service

```python
from captcha_solution import CaptchaSolver

solver = CaptchaSolver('anticaptcha', api_key='YOUR-API-KEY')
with open('captcha.png', 'rb') as inp:
    res = solver.solve(inp)
    print(res['solution'])
```

## Supported Captcha Services

* [2captcha.com](https://2captcha.com?from=3019071) (aka [rucaptcha.com](https://rucaptcha.com?from=3019071))
    * alias: `2captcha` and `rucaptcha`
    * docs (en): [https://2captcha.com/2captcha-api](https://2captcha.com/2captcha-api?form=3019071)
    * docs (ru): [https://rucaptcha.com/api-rucaptcha](https://rucaptcha.com/api-rucaptcha?form=3019071)

* [anti-captcha.com](http://getcaptchasolution.com/ijykrofoxz)
    * alias - `anticaptcha`
    * docs (en): [https://anticaptcha.atlassian.net/wiki/spaces/API/pages/196635/Documentation+in+English](https://anticaptcha.atlassian.net/wiki/spaces/API/pages/196635/Documentation+in+English)
    * docs (ru): [https://anticaptcha.atlassian.net/wiki/spaces/API/pages/196633](https://anticaptcha.atlassian.net/wiki/spaces/API/pages/196633)
