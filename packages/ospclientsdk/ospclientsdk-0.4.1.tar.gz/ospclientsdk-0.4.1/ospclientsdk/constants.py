"""ospclientsdk constants.
The constants module contains commonly used constants by ospclientsdk.
"""
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

__all__ = [
    "LOG_LEVELS",
    "LOG_FORMAT",
    "DEBUG_LOG_FORMAT"
]

LOG_LEVELS = {
    'debug': DEBUG,
    'info': INFO,
    'warning': WARNING,
    'error': ERROR,
    'critical': CRITICAL
}

LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

DEBUG_LOG_FORMAT = ("%(asctime)s %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
