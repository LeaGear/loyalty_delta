import json
from json import JSONDecodeError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from lp_backend.services import register_new_user, client_status
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