import datetime

from functools import wraps
from time import sleep


def with_retry(retries_and_sleep):
    retries, sleep_sec = retries_and_sleep or (3, 1)

    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                result = function(*args, **kwargs)
                if result:
                    return result
                sleep(sleep_sec)
        return wrapper
    return real_decorator


def paragraph_maker(*argv) -> str:
    msg = ''
    for arg in argv:
        msg += arg + "\n"
    return msg


def paragraph_maker_dict(dictionary: dict) -> str:
    msg = ''
    for key, value in dictionary.items():
        msg = f'{key}: {value}\n' + msg
    return msg


def print_log(log):
    now = datetime.datetime.now()
    now = now.strftime("%y/%m/%d %H:%M:%S - ") + log
    print(now)
