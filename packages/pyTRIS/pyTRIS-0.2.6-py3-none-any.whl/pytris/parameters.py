from datetime import datetime
from typing import Union


class Parameter:
    def __init__(self, name: str, required: bool):
        self.name = name
        self.required = required
    
    def to_value(self, value: Union[str, int]):
        return value


class DateParameter(Parameter):
    def to_value(self, value: Union[str, datetime]):
        if isinstance(value, datetime):
            return value.strtime('%d%m%Y')

        try:
            datetime.strptime(value, '%d%m%Y')
        except ValueError:
            raise ValueError(
                f'Parameter {self.name} must be of format DDMMYYYY '
                f'(received {value})'
            )

        return value
