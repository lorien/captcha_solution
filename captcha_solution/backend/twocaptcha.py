from .rucaptcha import RucaptchaBackend


class TwocaptchaBackend(RucaptchaBackend):
    base_url = 'https://2captcha.com'
