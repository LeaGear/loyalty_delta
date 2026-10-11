from django.db import IntegrityError

from lp_backend.models import Client, Operation, DiscountTier


def register_new_user(username, number, telegram_id):
    try:
        Client.objects.create(
            name=username,
            phone_number=number,
            telegram_id=telegram_id
        )
        return True
    except IntegrityError:
        return False

def client_exists(client_id):
    try:
        Client.objects.get(telegram_id=client_id)
        return True
    except Client.DoesNotExist:
        return False

def get_user_code(user_id):
    try:
        client = Client.objects.get(telegram_id=user_id)
    except Client.DoesNotExist:
        return None

    code = client.id  # TODO: In future returning code instead id
    return code

def get_user_data(user_id):
    try:
        client = Client.objects.get(telegram_id=user_id)
    except Client.DoesNotExist:
        return None
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