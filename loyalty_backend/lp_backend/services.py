from django.http import JsonResponse

from lp_backend.models import Client, Operation, DiscountTier


def register_new_user(username, number, telegram_id):
    try:
        Client.objects.create(
            name=username,
            phone_number=number,
            telegram_id=telegram_id
        )
        return JsonResponse({'status':'success', 'detail': 'Client registered'},status=200)
    except Exception as e:
        return JsonResponse({'status':'error', 'detail': str(e)}, status=400)

def client_status(client_id):
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

def get_user_code(user_id): #TODO: In future returning code instead id
    client = Client.objects.get(telegram_id=user_id)
    code = client.id
    return code

def get_user_data(user_id):
    client = Client.objects.get(telegram_id=user_id)
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