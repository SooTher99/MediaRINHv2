from fastapi import HTTPException


class RequestValidationError(HTTPException):
    def __init__(self, loc: list, msg: str, typ: str):
        super().__init__(400, [{'loc': loc, 'msg': msg, 'type': typ}])
