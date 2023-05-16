from pydantic import ConstrainedStr
from pydantic.types import _registered
from pydantic.typing import AnyCallable

import re
from typing import Type, Generator

from src.validators import empty_to_none

CallableGenerator = Generator[AnyCallable, None, None]


class ModificationConstrainedStr(ConstrainedStr):
    blank = False

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield from super().__get_validators__()
        yield empty_to_none


def constr(
    *,
    strip_whitespace: bool = False,
    to_upper: bool = False,
    to_lower: bool = False,
    strict: bool = False,
    min_length: int = None,
    max_length: int = None,
    curtail_length: int = None,
    regex: str = None,
    blank: bool = False
) -> Type[str]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        strip_whitespace=strip_whitespace,
        to_upper=to_upper,
        to_lower=to_lower,
        strict=strict,
        min_length=min_length,
        max_length=max_length,
        curtail_length=curtail_length,
        regex=regex and re.compile(regex),
        blank=blank,
    )
    return _registered(type('ConstrainedStrValue', (ModificationConstrainedStr,), namespace))