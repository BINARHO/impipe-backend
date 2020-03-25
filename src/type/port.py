from abc import ABC


class Port(ABC):
    def __init__(self, value=None, value_type=None):
        super(Port, self).__init__()

        self._validate_value(value, value_type)

        self._value = value
        self._value_type = value_type

    def _validate_value(self, value, value_type=None):
        pass

    def update_value(self, new_value):
        self._validate_value(new_value)
        self._value = new_value

    @property
    def value(self):
        return self._value
