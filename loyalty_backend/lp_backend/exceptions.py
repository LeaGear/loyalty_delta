

class ServiceError(Exception):
    """Base error business logic"""

class ClientNotFound(ServiceError):
    pass

class ClientAlreadyExists(ServiceError):
    pass

class CodeGenerationFailed(ServiceError):
    pass

class RegistrationError(ServiceError):
    pass

class ExpiredCode(ServiceError):
    pass

class IncorrectNumber(ServiceError):
    pass

class InvalidSearchInput(ServiceError):
    pass

class OperationAmountOverLimit(ServiceError):
    pass

class WrongOperationValue(ServiceError):
    pass

class NotExistForDeleting(ServiceError):
    pass

