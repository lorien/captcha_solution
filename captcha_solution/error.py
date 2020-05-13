class CaptchaSolutionError(Exception):
    pass


class RemoteServiceError(CaptchaSolutionError):
    pass


class UnexpectedServiceResponse(RemoteServiceError):
    pass


class ApiError(RemoteServiceError):
    def __init(self, msg, error_code):
        self.msg = msg
        self.error_code = error_code


class SolutionNotReady(ApiError):
    pass


class ZeroBalance(ApiError):
    pass


class NoSlotAvailable(ApiError):
    pass


class OperationTimeout(CaptchaSolutionError):
    pass


class ConfigurationError(CaptchaSolutionError):
    pass
