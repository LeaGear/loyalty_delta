

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
