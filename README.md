## Captcha Solution Python Package

Captcha Solution package is a simple interface to multiple captcha solving services.

## Image Captcha Example

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

## Custom Captcha Example
If you want to solve non-image type of captcha (text captcha, recaptcha, etc) you have to
use same solve method but pass the dict of parameters. Each captcha service has its own
parameters data schema so you need to consult with documentation to figure out the format of request

Say, we want to solve recaptcha. And we alredy obtained site key. Let's try two services:
2captcha.com and anti-captcha.com

In case of 2captcha, the documentation is
https://2captcha.com/2captcha-api?form=3019071#solving_recaptchav2_new
The list of POST parameters tells us there are required parameters: key, method, googlekey, pageurl.
You do not have to pass key, it is already done by solver. The call to method would be this:

```python
res = solver.solve({
  "method": "userrecaptcha",
  "googlekey": "VALUE-OF-SITE-KEY",
  "pageurl": "URL-OF-PAGE-WHERE-RECAPTCHA-IS-DISPLAYED"
})
print('Solution: %s' % res['solution'])
print('Raw Response: %s' % res['raw'])

In case of anti-captcha, the documentation is here https://anticaptcha.atlassian.net/wiki/spaces/API/pages/5079084/Captcha+Task+Types
Required keys for NoCaptchaTaskProxyless request are type, websiteURL, websiteKey
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
