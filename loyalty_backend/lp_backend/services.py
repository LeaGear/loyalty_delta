import secrets

from django.db import IntegrityError, transaction
from django.utils import timezone

from lp_backend.models import Client, Operation, DiscountTier
from lp_backend.constants import CODE_TTL, CODE_LENGTH
from lp_backend.exceptions import ClientNotFound, ClientAlreadyExists, CodeGenerationFailed, RegistrationError


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

        if client.actual_code and client.code_expires_at and client.code_expires_at > now:
            return client.actual_code

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


def get_actual_discount(total_spent):
    discount = DiscountTier.objects.filter(min_total__lte=total_spent).first()
    return discount