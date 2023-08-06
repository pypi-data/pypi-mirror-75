from functools import wraps
from typing import Any, Type, Callable
from datetime import datetime, time, date


def parse(target_type: Type, string: str, fallback=None, decimal_separator=".") -> Any:
    try:
        if target_type == float and decimal_separator != ".":
            string = string.replace(decimal_separator, ".")

        return target_type(string)
    except ValueError:
        return fallback


def coalesce(*args) -> Any:
    if args is None:
        return None

    for item in args:
        if item is not None:
            return item
    return None


def start_of_day(input_date: date) -> datetime:
    return datetime.combine(input_date, time())


def require(**kwargs):
    def inner(func):
        @wraps(func)
        def innermost(*args, **kwargs2):

            for attr in kwargs.__dict__:
                pass
            return func(*args, **kwargs2)

        return innermost

    return inner


@require(xDD=lambda x: x > 3)
def end_of_day(input_date: date) -> datetime:
    return datetime.combine(input_date, time(23, 59, 59, 59))


end_of_day(datetime.today())
