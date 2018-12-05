import string
from random import sample

import config

letters = list(string.ascii_letters)
number = [str(i) for i in range(10)]
letters.extend(number)


def get_captcha(num=config.CAPTCHA_NUM):
    return ''.join(sample(letters, num))


