import json
from json import JSONDecodeError

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from lp_backend.api.decorators import api_key_required
from lp_backend.services import register_new_user, validate_client_exists, generate_user_code, get_client_data, \
    get_client_by_tg_id
from lp_backend.api.responses import ok, fail
from lp_backend.exceptions import ClientNotFound, CodeGenerationFailed, RegistrationError, ClientAlreadyExists


# Create your views here.

@csrf_exempt
@require_POST
@api_key_required
def registration_user_view(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return fail(detail='Invalid JSON', status_code=400)

    if not isinstance(data, dict):
        return fail(detail='Invalid JSON format', status_code=400)

    user_name = (data.get('user_name') or '').strip()
    user_phone = data.get('phone_number')
    try:
        user_id = int(data.get('telegram_id'))
    except (ValueError, TypeError):
        return fail(detail='Invalid Telegram ID', status_code=400)

    if not(user_name and user_phone and user_id) or len(user_name) > 100:
        return fail(detail='Missing required fields', status_code=400)

    try:
        register_new_user(user_name, user_phone, user_id)
        return ok(detail='User successfully registered', status_code=201)
    except ClientAlreadyExists:
        return fail(detail='User already exists', status_code=409)
    except RegistrationError:
        return fail(detail='User cannot be registered', status_code=400)

@require_GET
@api_key_required
def check_user_status_view(request, user_id):
    try:
        validate_client_exists(user_id)
        return ok(detail='User is registered', status_code=200)
    except ClientNotFound:
        return fail(detail='User not found in DB', status_code=404)

@require_GET
@api_key_required
def get_user_loyalty_code_view(request, user_id):
    try:
        code = generate_user_code(user_id)
        return ok(detail='User loyalty code received: type -> string', data=code, status_code=200)
    except CodeGenerationFailed:
        return fail(detail='Code generation Error', status_code=503)
    except ClientNotFound:
        return fail(detail='User not found in DB', status_code=404)

@require_GET
@api_key_required
def get_user_data_view(request, user_id):
    try:
        inner_id = get_client_by_tg_id(user_id)
        data = get_client_data(inner_id.id)
        return ok(detail='User data received: type -> dict', data=data, status_code=200)
    except ClientNotFound:
        return fail(detail='User not found in DB', status_code=404)
