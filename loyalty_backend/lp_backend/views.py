from django.http import JsonResponse

from lp_backend.services import register_new_user
# Create your views here.

def test_view(request):
    if request.method == 'POST':
        # Здесь ваша логика обработки
        return JsonResponse({'status': 'success', 'message': 'Данные приняты!'})

    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=400)

def registration_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        number = request.POST.get('phone_number')
        telegram_id = request.POST.get('telegram_id')
        register_new_user(username, number, telegram_id)
        return ('success')

    return ('error')