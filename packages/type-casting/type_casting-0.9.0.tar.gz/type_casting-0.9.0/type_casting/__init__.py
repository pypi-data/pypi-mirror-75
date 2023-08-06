import sys


__version__ = "0.9.0"


if sys.version_info.major == 3 and sys.version_info.minor == 7:
    from .py37 import GetAttr, cast
else:  # sys.version_info.major == 3 and sys.version_info.minor == 8
    from .latest import GetAttr, cast
