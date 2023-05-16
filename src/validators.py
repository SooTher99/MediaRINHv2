from pydantic.fields import ModelField
from pydantic.types import errors

def empty_to_none(v: str, field: 'ModelField') -> str | None:
    if not field.type_.blank and v == '' :
        if not field.allow_none:
            raise errors.NoneIsNotAllowedError()
        else:
            return None
    return v
