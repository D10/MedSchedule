from enum import Enum


class LogFormat(str, Enum):
    plain = "plain"
    json = "json"
