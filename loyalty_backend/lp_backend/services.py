
from django.db import transaction
from django.http import JsonResponse

from lp_backend.models import Client, Operation


def register_new_user(username, number, telegram_id):
    try:
        Client.objects.create(
            name=username,
            phone_number=number,
            telegram_id=telegram_id
        )
        return JsonResponse({'status':'success', 'detail': 'Client registered'},status=200)
    except Exception as e:
        return JsonResponse({'status':'error', 'detail': str(e)},status=400)

def get_user_discount_code():
    pass

def add_new_operation():
    pass

def client_status(client_id):
    print(client_id)
    try:
        Client.objects.get(telegram_id=client_id)
        return JsonResponse({
                'status':'success',
                'detail':'Client is registered'
            },status=200)
    except Client.DoesNotExist:
        return JsonResponse({
                'status':'error',
                'detail':'Client is not registered'
            },status=404)