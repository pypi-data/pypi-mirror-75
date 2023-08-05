

class ApiException(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        if isinstance(message, dict):
            self.message = message
            self.message["code"] = self.__class__.__name__
        else:
            self.message = {
                "code": self.__class__.__name__,
                "text": message
            }
        self.status = status
