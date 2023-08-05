# -*- coding: UTF-8 -*-
"""
Certain services related stuff
"""

import enum
# pylint: disable=import-self
from . import anti_captcha, deathbycaptcha, rucaptcha, twocaptcha


class CaptchaSolvingService(enum.Enum):
    """ CAPTCHA solving service enumeration """

    ANTI_CAPTCHA = "anti-captcha.com"
    DEATHBYCAPTCHA = "deathbycaptcha.com"
    RUCAPTCHA = "rucaptcha.com"
    TWOCAPTCHA = "2captcha.com"


# supported CAPTCHA solving services
SOLVING_SERVICE = {
    CaptchaSolvingService.ANTI_CAPTCHA: anti_captcha,
    CaptchaSolvingService.DEATHBYCAPTCHA: deathbycaptcha,
    CaptchaSolvingService.RUCAPTCHA: rucaptcha,
    CaptchaSolvingService.TWOCAPTCHA: twocaptcha
}
