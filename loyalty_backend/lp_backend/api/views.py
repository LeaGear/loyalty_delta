import json
from json import JSONDecodeError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from lp_backend.services import register_new_user, client_status, get_user_code, get_user_data
# Create your views here.

@csrf_exempt
@require_POST
def registration_user_view(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'status': 'error', 'detail': 'Invalid JSON'}, status=400)
    response = register_new_user(data.get('user_name'), data.get('phone_number'), data.get('telegram_id'))
    return response

@require_GET
def check_user_status_view(request, user_id):
    result = client_status(user_id)
    return result

@require_GET
def get_user_loyalty_code_view(request, user_id):
    code = get_user_code(user_id)
    return JsonResponse({'status': 'success', 'data': code}, status=200)

@require_GET
def get_user_data_view(request, user_id):
    data = get_user_data(user_id)
    return JsonResponse({'status': 'success', 'detail':'', 'data': data}, status=200)
