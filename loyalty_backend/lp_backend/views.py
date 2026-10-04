from django.shortcuts import render

from pl_backend.services import register_new_user
# Create your views here.

def register_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        number = request.POST.get('phone_number')
        telegram_id = request.POST.get('telegram_id')
        register_new_user(username, number, telegram_id)
        return ('success')

    return ('error')