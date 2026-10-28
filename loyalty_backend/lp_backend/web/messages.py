
from lp_backend.exceptions import ExpiredCode, CodeGenerationFailed, \
    RegistrationError, IncorrectNumber, ClientNotFound, ClientAlreadyExists, OperationAmountOverLimit, \
    InvalidSearchInput, WrongOperationValue, NotExistForDeleting, InvalidNote

ERROR_TEXTS = {
    ExpiredCode: "Code has expired, ask the client to generate a new one.",
    ClientNotFound: "Client not found.",
    ClientAlreadyExists: "Client already exists.",
    CodeGenerationFailed: "Code generation failed.",
    RegistrationError: "Registration failed.",
    IncorrectNumber: "Phone number format is incorrect.",
    InvalidSearchInput: "Enter an ID, a phone number or a code.",
    OperationAmountOverLimit: "Amount is too large.",
    WrongOperationValue: "Wrong add_operation value.",
    NotExistForDeleting: "Record was not deleted. Not found in DB",
    InvalidNote: "Note has been sent without message"
}

def error_text(exc):
    return ERROR_TEXTS.get(type(exc), "Something went wrong(")
