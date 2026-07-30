"""
AIOS Version Manager

Single source of truth.
"""

AIOS_NAME = "AIOS"

PROJECT = "Artificial Intelligence Operating System"

AUTHOR = "Rudolph"

AIOS_VERSION = "0.9.5"

STAGE = "alpha"

BUILD = 1

BUILD_DATE = "2026-07-17"

PYTHON_VERSION = "3.14.6"

FULL_VERSION = f"{AIOS_VERSION}-{STAGE}.{BUILD}"


def version() -> str:

    return FULL_VERSION

_all_ = [
    "AIOS_NAME",
    "PROJECT",
    "AUTHOR",
    "AIOS_VERSION",
    "STAGE",
    "BUILD",
    "BUILD_DATE",
    "PYTHON_VERSION",
    "FULL_VERSION",
    "version",
]