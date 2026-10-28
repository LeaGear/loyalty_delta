import secrets
from datetime import datetime

from django.db import IntegrityError, transaction
from django.db.models import Sum, Q
from django.utils import timezone
from zoneinfo import ZoneInfo

from lp_backend.models import Client, Operation, DiscountTier, ClientNote, OperationType
from lp_backend.constants import CODE_TTL, CODE_LENGTH, MAXIMUM_DISCOUNT_VALUE
from lp_backend.exceptions import ClientNotFound, ClientAlreadyExists, CodeGenerationFailed, RegistrationError, \
    ExpiredCode, IncorrectNumber, InvalidSearchInput, OperationAmountOverLimit, WrongOperationValue, \
    NotExistForDeleting, InvalidNote


def _code_is_actual(code_expires_at) -> bool:
    now = timezone.now()
    if code_expires_at and now < code_expires_at:
        return True
    else:
        return False

def _get_client_by_inner_id(inner_id) -> Client:
    try:
        client = Client.objects.get(id=inner_id)
        return client
    except Client.DoesNotExist:
        raise ClientNotFound(inner_id)

def _get_actual_discount(total_spent) -> DiscountTier:
    discount = DiscountTier.objects.filter(min_total__lte=total_spent).first()
    return discount

def _get_last_actual_operation_date(client_id) -> datetime | None:
    last_operation = Operation.objects.filter(client_id=client_id).order_by('-operation_date').first()
    if not last_operation:
        return None
    return last_operation.operation_date

def _get_overall_discount(db_percent, custom_bonus) -> int:
    summary = db_percent + custom_bonus
    overall = min(MAXIMUM_DISCOUNT_VALUE, summary)
    return overall

def _change_time_to_actual_tz(date: datetime) -> str | None:
    if not date:
        return None

    kyiv_tz = ZoneInfo("Europe/Kyiv")
    pd_kyiv = date.astimezone(kyiv_tz)
    actual = pd_kyiv.strftime('%d-%m-%Y %H:%M')
    return actual

def _calculate_client_total_spent(client) -> None:
    result = Operation.objects.filter(client=client).aggregate(
        total_purchases=Sum('amount', filter=Q(operation_type=OperationType.PURCHASE)),
        total_refunds=Sum('amount', filter=Q(operation_type=OperationType.REFUND)),
    )
    purchase_sum = result['total_purchases'] or 0
    refund_sum = result['total_refunds'] or 0
    total_spent = max(purchase_sum - refund_sum, 0)
    client.set_total_spent(total_spent)

def register_new_user(username, number, telegram_id) -> None:
    try:
        Client.objects.create(
            name=username,
            phone_number=number,
            telegram_id=telegram_id
        )
    except IntegrityError:
        raise ClientAlreadyExists(telegram_id)
    except Exception as e:
        raise RegistrationError(telegram_id) from e

def validate_client_exists(client_id) -> None:
    try:
        Client.objects.get(telegram_id=client_id)
    except Client.DoesNotExist:
        raise ClientNotFound(client_id)

def generate_user_code(user_id) -> str:
    now = timezone.now()
    expires_time = now + CODE_TTL

    with transaction.atomic():
        try:
            client = Client.objects.select_for_update().get(telegram_id=user_id)
        except Client.DoesNotExist:
            raise ClientNotFound(user_id)
        if _code_is_actual(client.code_expires_at):
            return client.actual_code
        else:
            for _ in range(5):
                code = f"{secrets.randbelow(10**CODE_LENGTH):0{CODE_LENGTH}d}"
                try:
                    with transaction.atomic():
                        client.change_code(code, expires_time)
                    return code
                except IntegrityError:
                    continue

    raise CodeGenerationFailed


def get_client_by_tg_id(telegram_id) -> Client:
    try:
        client = Client.objects.get(telegram_id=telegram_id)
        return client
    except Client.DoesNotExist:
        raise ClientNotFound(telegram_id)

def get_client_id_by_param(client_param) -> int:
    digits = "".join(ch for ch in client_param if ch.isdigit())
    if not digits:
        raise InvalidSearchInput(client_param)

    try:
        if len(digits) == CODE_LENGTH:
            client = Client.objects.get(actual_code=digits)
            if not _code_is_actual(client.code_expires_at):
                raise ExpiredCode()
            return client.id

        elif len(digits) in (10,12):
            if len(digits) == 12 and digits.startswith("380"):
                number = digits
            elif len(digits) == 10 and digits.startswith("0"):
                number = "38" + digits
            else:
                raise IncorrectNumber(digits)
            client = Client.objects.get(phone_number=number)
            return client.id

        elif len(digits) < CODE_LENGTH: #TODO: Search by ID only for admin
            client = _get_client_by_inner_id(int(digits))
            return client.id

    except Client.DoesNotExist:
        raise ClientNotFound(client_param)

    raise InvalidSearchInput(client_param)


def get_client_data(db_inner_id) -> dict:
    client = _get_client_by_inner_id(db_inner_id)
    actual_discount = _get_actual_discount(client.total_spent)
    user_data = {
        'id': client.id,
        'name': client.name,
        'phone_number': client.phone_number,
        'code': client.actual_code if _code_is_actual(client.code_expires_at) else "---",
        'total_spent': client.total_spent,
        'discount_level': actual_discount.name,
        'discount': actual_discount.discount_percent,
        'custom_discount': client.custom_discount,
        'overall_discount': _get_overall_discount(actual_discount.discount_percent, client.custom_discount), #actual_discount.discount_percent + client.custom_discount,
        'last_operation_date': _change_time_to_actual_tz(client.last_operation_date)#client.last_operation_date
    }
    return user_data

def get_all_client_notes(client_id) -> list:
    result = []
    notes = ClientNote.objects.filter(client_id=client_id)
    for note in notes:
        actual_time = _change_time_to_actual_tz(note.created_at)
        temp = {
            'id': note.id,
            'date': actual_time,
            'text' : note.text
        }
        result.append(temp)
    return result

def get_all_client_operations(client_id) -> list:
    result = []
    operations = Operation.objects.filter(client_id=client_id)
    for oper in operations:
        actual_time = _change_time_to_actual_tz(oper.operation_date)
        temp = {
            'id' : oper.id,
            'amount' : oper.amount,
            'type' : oper.operation_type,
            'date' : actual_time
        }
        result.append(temp)
    return result

def add_new_note(client_id, note_text):
    if not note_text:
        raise InvalidNote
    try:
        ClientNote.objects.create(
            client_id=client_id,
            text=note_text,
        )
    except IntegrityError:
        raise ClientNotFound(client_id)

def delete_note(note_id, client_id):
    deleted_count, details = ClientNote.objects.filter(id=note_id, client_id=client_id).delete()
    if deleted_count > 0:
        print("Deleted records -> ", details) #TODO: logger info
    else:
        raise NotExistForDeleting(note_id)

@transaction.atomic
def add_new_operation(operation_amount, operation_type, client_id):
    if not operation_amount or not float(operation_amount):
        raise WrongOperationValue()
    if len(operation_amount) > 5:
        raise OperationAmountOverLimit()
    try:
        client = Client.objects.select_for_update().get(id=client_id)
    except Client.DoesNotExist:
        raise ClientNotFound(client_id)

    if operation_type == "purchase":
        Operation.objects.create(
            client=client,
            operation_type=OperationType.PURCHASE,
            amount=operation_amount
        )
    elif operation_type == "refund":
        Operation.objects.create(
            client=client,
            operation_type=OperationType.REFUND,
            amount=operation_amount
        )
    else:
        raise WrongOperationValue(operation_type)

    last_operation_date = _get_last_actual_operation_date(client_id)
    client.set_last_operation_date(last_operation_date)
    _calculate_client_total_spent(client)

@transaction.atomic
def delete_operation(operation_id, client_id):
    try:
        client = Client.objects.select_for_update().get(id=client_id)
    except Client.DoesNotExist:
        raise ClientNotFound(client_id)
    deleted_count, details = Operation.objects.filter(id=operation_id, client=client).delete()
    if deleted_count > 0:
        last_operation_date = _get_last_actual_operation_date(client_id)
        client.set_last_operation_date(last_operation_date)
        _calculate_client_total_spent(client)
        print("Deleted records -> ", details) #TODO: logger info
    else:
        raise NotExistForDeleting(operation_id)