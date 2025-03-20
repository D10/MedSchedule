import functools

from .sctruct_log import setup_struct_logger

setup_logging = functools.partial(setup_struct_logger)
