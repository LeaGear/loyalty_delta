import secrets

from django.db import IntegrityError, transaction
from django.utils import timezone
from psycopg import Transaction

from lp_backend.models import Client, Operation, DiscountTier, ClientNote, OperationType
from lp_backend.constants import CODE_TTL, CODE_LENGTH
from lp_backend.exceptions import ClientNotFound, ClientAlreadyExists, CodeGenerationFailed, RegistrationError, \
    ExpiredCode

def user_data_dict_builder(client):
    result = {
        'name': client.name,
        'id': client.id,
        'code': client.actual_code if client.actual_code else "",
        'phone_number': client.phone_number,
        'total_spent': float(client.total_spent),
        'discount': get_actual_discount(client.total_spent, client.custom_discount),
        'transactions': get_all_client_transactions(client),
        'notes': get_all_client_notes(client)
    }
    return result


def code_is_actual(code_expires_at):
    now = timezone.now()
    expires_time = now + CODE_TTL
    if code_expires_at and now < code_expires_at < expires_time:
        return True
    else:
        return False

def get_client_by_parameters(client_id=0, code='', number=''):
    client = None

    try:
        client = Client.objects.get(id=client_id)
        return client
    except Client.DoesNotExist:
        pass

    try:
        client = Client.objects.get(phone_number=number)
        return client
    except Client.DoesNotExist:
        pass

    try:
        client = Client.objects.get(actual_code=code)
        if code_is_actual(client.code_expires_at):
            return client
        else:
            raise ExpiredCode()
    except Client.DoesNotExist:
        pass

    if not client:
        raise ClientNotFound("All parameters - unavailable")

    return client

def register_new_user(username, number, telegram_id):
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

def client_status(client_id):
    try:
        Client.objects.get(telegram_id=client_id)
    except Client.DoesNotExist:
        raise ClientNotFound(client_id)

def get_user_code(user_id):
    now = timezone.now()
    expires_time = now + CODE_TTL

    with transaction.atomic():
        try:
            client = Client.objects.select_for_update().get(telegram_id=user_id)
        except Client.DoesNotExist:
            raise ClientNotFound(user_id)
        if code_is_actual(client.code_expires_at):
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

def get_user_data(user_id):
    try:
        client = Client.objects.get(telegram_id=user_id)
    except Client.DoesNotExist:
        raise ClientNotFound(user_id)
    actual_discount = get_actual_discount(client.total_spent)
    user_data = {
        'name': client.name,
        'phone_number': client.phone_number,
        'total_spent': client.total_spent,
        'discount_level': actual_discount.name,
        'discount': actual_discount.discount_percent,
        'last_visit': client.last_operation_date
    }
    return user_data


def get_actual_discount(total_spent, custom_discount):
    discount = get_discount(total_spent).discount_percent
    return discount + custom_discount

def get_discount(total_spent):
    discount = DiscountTier.objects.filter(min_total__lte=total_spent).first()
    return discount

def get_client_data(search_data):
    web_code = search_data.get("code").strip()
    web_id = int(search_data.get("id").strip())
    web_number = search_data.get("number").strip()

    client = get_client_by_parameters(client_id=web_id, code=web_code, number=web_number)
    if client:
        return user_data_dict_builder(client)
    else:
        raise ClientNotFound(search_data)

def add_new_note(note_data):
    client_id = int(note_data.get("client_id").strip())
    note_text = note_data.get("new-note").strip()

    client = get_client_by_parameters(client_id=client_id)

    ClientNote.objects.create(
        client=client,
        text=note_text,
    )
    return user_data_dict_builder(client)

def delete_note(note_data):
    client_id = int(note_data.get("client_id").strip())
    note_id = int(note_data.get("note_id").strip())
    ClientNote.objects.filter(id=note_id).delete()
    client = get_client_by_parameters(client_id=client_id)
    return user_data_dict_builder(client)

def add_new_transaction(note_data):
    if not note_data.get("transaction-amount").strip():
        return None
    client_id = int(note_data.get("client_id").strip())
    transaction_amount = float(note_data.get("transaction-amount").strip())
    transaction_type = note_data.get("trans-type").strip()


    client = get_client_by_parameters(client_id=client_id)

    if transaction_type == "purchase":
        Operation.objects.create(
            client=client,
            operation_type=OperationType.PURCHASE,
            amount=transaction_amount,
        )
    else:
        Operation.objects.create(
            client=client,
            operation_type=OperationType.REFUND,
            amount=transaction_amount,
        )

    return user_data_dict_builder(client)

def get_all_client_notes(client):
    result = []
    notes = ClientNote.objects.filter(client=client)
    for note in notes:
        temp = {
            'id': note.id,
            'text' : f"[{note.created_at.strftime('%d-%m-%Y %H:%M')}] {note.text}"
        }
        result.append(temp)
    return result

def get_all_client_transactions(client):
    result = []
    transactions = Operation.objects.filter(client=client)
    for trans in transactions:
        temp = f"[{trans.operation_date.strftime('%d-%m-%Y %H:%M')}] [{trans.operation_type}] <------> {trans.amount}"
        result.append(temp)

    return result