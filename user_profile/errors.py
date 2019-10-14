class BaseError(Exception):
    default_message = 'Something went wrong'

    def __init__(self, message=None):
        self._message = message

    @property
    def message(self):
        return self._message or self.default_message


class DuplicateUserError(BaseError):
    default_message = 'This users already exists'
