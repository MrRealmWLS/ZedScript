
class Error():
    def __init__(self, error, about):
        self.error = error
        self.about = about

    def zed_raise(self, line_number=None):
        error_message = f"{self.error}: {self.about}"
        if line_number is not None:
            error_message += f"occurred on line {line_number}"
        raise Exception(error_message)


class SyntaxError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("SyntaxError", about)
        self.zed_raise(line_number)
class TypeError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("TypeError", about)
        self.zed_raise(line_number)

class UnknownTypeError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("UnknowTypeError", about)
        self.zed_raise(line_number)
class UnknowDependenciesError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("UnknowDependenciesError", about)
        self.zed_raise(line_number)
class InvalidCharactersError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("InvalidCharactersError", about)
        self.zed_raise(line_number)
class ImportError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("ImportError", about)
        self.zed_raise(line_number)
class VauleError(Error):
    def __init__(self, about, line_number=None):
        super().__init__("VauleError", about)
        self.zed_raise(line_number)