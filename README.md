## Captcha Solution Python Package

Captcha Solution package is a simple interface to multiple captcha solving services.

## Simple Image Captcha

The simplest case is to solve captcha image stored into file.
Pass the file handler to the `solve` method. The solution will
be stored into "solution" key of returned result. In "raw" key
there is a full original response that captcha service returned.

```python
from captcha_solution import CaptchaSolver

solver = CaptchaSolver('anticaptcha', api_key='YOUR-API-KEY')
with open('captcha.png', 'rb') as inp:
    res = solver.solve(inp)
    print(res['solution'])
```

## Custom Captcha

If you want to solve non-image type of captcha (text captcha, recaptcha, etc) you have to
use same `solve` method but you need to pass the dict of parameters. Each captcha service has its own
request data schema so you need to consult with documentation to figure out format of request

## Example, solving recaptcha with 2captcha.com

Documentation is [https://2captcha.com/2captcha-api?form=3019071#solving_recaptchav2_new](https://2captcha.com/2captcha-api?form=3019071#solving_recaptchav2_new?from=3019071)

Required POST parameters are: key, method, googlekey, pageurl.
You do not have to pass key (api key), it is already done by solver. The code would be like:

```python
res = solver.solve({
  "method": "userrecaptcha",
  "googlekey": "VALUE-OF-SITE-KEY",
  "pageurl": "URL-OF-PAGE-WHERE-RECAPTCHA-IS-DISPLAYED"
})
print('Solution: %s' % res['solution'])
print('Raw Response: %s' % res['raw'])
```

## Example, solving recaptcha with anti-captcha.com

Documentation is https://anticaptcha.atlassian.net/wiki/spaces/API/pages/5079084/Captcha+Task+Types
We need to use NoCaptchaTaskProxyless type of task.
This task requires to provide at least these keys: type, websiteURL, websiteKey
Code will looks like:
```python
res = solver.solve({
  "type": "NoCaptchaTaskProxyless",
  "websiteKEY": "VALUE-OF-SITE-KEY",
  "websiteURL": "URL-OF-PAGE-WHERE-RECAPTCHA-IS-DISPLAYED"
})
print('Solution: %s' % res['solution'])
print('Raw Response: %s' % res['raw'])
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
