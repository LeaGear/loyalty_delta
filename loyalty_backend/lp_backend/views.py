import json
from json import JSONDecodeError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from lp_backend.services import register_new_user, client_status, get_user_code, get_user_data
# Create your views here.

def test_view(request):
    if request.method == 'GET':
        # Здесь ваша логика обработки
        return JsonResponse({'status': 'success', 'message': 'Данные приняты!'})

    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=400)

@csrf_exempt
def registration_user_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
        except JSONDecodeError:
            return JsonResponse({'status': 'error', 'detail': 'Invalid JSON'}, status=400)
        response = register_new_user(data.get('user_name'), data.get('phone_number'), data.get('telegram_id'))
        return response
    return JsonResponse({'status': 'error', 'detail': 'Method not allowed'}, status=400)

def check_user_status_view(request, user_id):
    if request.method == 'GET':
        result = client_status(user_id)
        return result
    return JsonResponse({'status': 'error', 'detail': 'Method not allowed'}, status=400)

def get_user_loyalty_code_view(request, user_id):
    if request.method == 'GET':
        code = get_user_code(user_id)
        return JsonResponse({'status': 'success', 'data': code}, status=200)
    return JsonResponse({'status': 'error', 'detail': 'Method not allowed'}, status=400)

def get_user_data_view(request, user_id):
    if request.method == 'GET':
        data = get_user_data(user_id)
        print(f"view data: {data}")
        return JsonResponse({'status': 'success', 'detail':'', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'detail': 'Method not allowed', 'data': None}, status=400)