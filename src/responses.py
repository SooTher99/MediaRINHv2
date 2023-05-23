from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from conf.settings import settings

TemplateResponse = Jinja2Templates(directory=settings.TEMPLATES_DIR).TemplateResponse


class RequestValidationError(HTTPException):
    def __init__(self, loc: list, msg: str, typ: str):
        super().__init__(400, [{'loc': loc, 'msg': msg, 'type': typ}])
