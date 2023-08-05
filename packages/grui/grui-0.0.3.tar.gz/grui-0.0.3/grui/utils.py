import re

_dash_case_regex = (re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))'), re.compile('_+'))


def dash_case(string: str):
    return _dash_case_regex[1].sub("-", _dash_case_regex[0].sub(r'-\1', string).lower())
