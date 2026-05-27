class AppException(Exception):
    """Base application exception."""

class InvalidCredentialsException(AppException):
    pass

class EmailAlreadyRegisteredException(AppException):
    pass

class UnauthorizedException(AppException):
    pass

class UserNotFoundException(AppException):
    pass