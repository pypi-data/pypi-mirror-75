"""
typhoon.util module
"""
import hashlib
import re
import socket
import sys
import threading
import time


def _get_host() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class RecordId(object):
    """
    Record id generator.
    """

    def __init__(self) -> None:
        self.host = _get_host()
        self.count = 0
        self.main_path = sys.argv[0]

    def __call__(self) -> str:
        self.count += 1
        hl = hashlib.md5()
        string = self.host + self.main_path + \
            str(time.time()) + str(id(hl)) + str(self.count)
        hl.update(string.encode(encoding='utf-8'))
        return hl.hexdigest()


class TraceId(threading.local):
    """
    Trace id manager.
    """

    def __call__(self) -> str:
        return getattr(self, 'traceId', '-')

    def set_trace(self, trace_id: str) -> None:
        setattr(self, 'traceId', trace_id)

    def del_trace(self) -> None:
        delattr(self, 'traceId')


def camel_to_snake(camelCase: str) -> str:
    """
    convert CamelCase string into snake_case string.
    """
    pattern = re.compile(r'([a-z]|\d)([A-Z])')
    snake_case = re.sub(
        pattern=pattern,
        repl=r'\1_\2',
        string=camelCase).lower()
    return snake_case


def snake_to_camel(snake_case: str) -> str:
    """
    convert snake_case string into CamelCase string.
    """
    pattern = re.compile(r'(_\w)')
    camelCase = re.sub(
        pattern=pattern,
        repl=lambda s: s.group(1)[1].upper(),
        string=snake_case
    )
    return camelCase


def json_camel_to_snake(camelCaseJsonStr: str) -> str:
    """
    convert CamelCase keys inside a json string into snake_case keys.
    """
    pattern = re.compile(r'"\s*(\w+)\s*"\s*:')
    snake_case_json_str = re.sub(
        pattern=pattern,
        repl=lambda s: '"' + camel_to_snake(s.group(1)) + '":',
        string=camelCaseJsonStr
    )
    return snake_case_json_str


def json_snake_to_camel(snake_case_json_str: str) -> str:
    """
    convert snake_case keys inside a json string into CamelCase keys.
    """
    pattern = re.compile(r'"\s*(\w+)\s*"\s*:')
    camelCaseJsonStr = re.sub(
        pattern=pattern,
        repl=lambda s: '"' + snake_to_camel(s.group(1)) + '":',
        string=snake_case_json_str
    )
    return camelCaseJsonStr


def get_banner(version: str) -> str:
    """
    get banner of typhoon.
    """
    version = f' v{version} '
    lines = [
        "",
        "=" * 48,
        "    _____            _ ",
        "   |_   _|   _ _ __ | |__  based on Tornado",
        "     | || | | | '_ \| '_ \ / _ \ / _ \| '_ \ ",
        "     | || |_| | |_) | | | | (_) | (_) | | | |",
        "     |_| \__, | .__/|_| |_|\___/ \___/|_| |_|",
        "         |___/|_|",
        f"{version:=>45s}===",
    ]
    return '\n'.join(lines)
