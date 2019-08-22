# services/citizens/project/schemas/validation.py
from jsonschema import validate, ValidationError, FormatChecker
from project.schemas import schemas
import datetime


# Валидация даты
@FormatChecker.cls_checks('date')
def date_check(value):
    date_format = '%d.%m.%Y'
    try:
        datetime.datetime.strptime(value, date_format)
    except ValueError:
        return False
    return True


# Проверка формата запроса
def schema_validate(request, schema):
    try:
        validate(instance=request, schema=schemas[schema], format_checker=FormatChecker())
    except ValidationError as e:
        return 'ValidationError: %s' % (e,)
    return None
