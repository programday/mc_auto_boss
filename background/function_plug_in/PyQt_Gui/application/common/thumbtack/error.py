class ProvideError(Exception):

    def __init__(self, base_error: Exception, *args: object) -> None:
        super().__init__(*args)
        self.with_traceback(base_error.__traceback__)


class InjectionError(Exception):

    def __init__(self, base_error: Exception, *args: object) -> None:
        super().__init__(*args)
        self.with_traceback(base_error.__traceback__)
