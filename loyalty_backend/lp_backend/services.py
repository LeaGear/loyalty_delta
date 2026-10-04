
from django.db import transaction
from lp_backend.models import Client, Operation


def register_new_user(username, number, telegram_id):
    Client.objects.create(
        name=username,
        phone_number=number,
        telegram_id=telegram_id
    )

def get_user_discount_code():
    pass

def add_new_operation():
    pass