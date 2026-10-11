import json
from json import JSONDecodeError

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from lp_backend.services import register_new_user, client_exists, get_user_code, get_user_data
from lp_backend.api.responses import ok, fail

# Create your views here.

#TODO: NEXT STEP - SERVICES = DATA || VIEWS = JSON
@csrf_exempt
@require_POST
def registration_user_view(request):
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            return fail('Invalid JSON format', 400)
    except JSONDecodeError:
        return fail('Invalid JSON', 400)

    user_name = (data.get('user_name') or '').strip()
    user_phone = data.get('phone_number')
    try:
        user_id = int(data.get('telegram_id'))
    except (ValueError, TypeError):
        return fail('Invalid Telegram ID', 400)

    if not(user_name and user_phone and user_id) or len(user_name) > 100:
        return fail('Missing required fields', 400)

    response = register_new_user(user_name, user_phone, user_id)

    if response is True:
        return ok('User successfully registered', status_code=201)

    else:
        return fail('User cannot be registered', 409)

@require_GET
def check_user_status_view(request, user_id):
    result = client_exists(user_id)
    if result:
        return ok('User is registered', status_code=200)
    else:
        return fail('User not found in DB', 404)

@require_GET
def get_user_loyalty_code_view(request, user_id):
    code = get_user_code(user_id)
    if code is None:
        return fail('User not found in DB', 404)
    return ok('User loyalty code received: type -> int', code,  200)

@require_GET
def get_user_data_view(request, user_id):
    data = get_user_data(user_id)
    if data is None:
        return fail('User not found in DB', 404)
    return ok('User data received: type -> dict', data, 200)
