
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render

from lp_backend.services import get_client_data, add_new_note

# TODO: TEST
USER_INFO_TEST = {
    'id': 12551512,
    'name': 'Duha',
    'code': 125135561,
    'number': '142352352',
    'notes': ['biba', 'asdasd', 'boba', 'hupe', 'asdasd', 'asdasdgfder','biba', 'asdasd', 'boba', 'hupe', 'asdasd', 'asdasdgfder','biba', 'asdasd', 'boba', 'hupe', 'asdasd', 'asdasdgfder']
}
'''{
    'name': client.name,
    'id':client.id,
    'code': client.actual_code,
    'phone_number': client.phone_number,
    'total_spent': client.total_spent,
    'discount': get_actual_discount(client.total_spent).discount_percent
}'''

@require_GET
def base_view(request):
    return render(request, 'lp_backend/vendors/client_checking.html')


@require_GET
def search_client_view(request):
    search_data = request.GET.dict()
    print(search_data)
    user_data = get_client_data(search_data)
    print(user_data)
    return render(request, 'lp_backend/vendors/client_checking.html', {'user_info': user_data})

@require_GET
def add_note_view(request):
    new_note_data = request.GET.dict()
    print(new_note_data)
    user_data = add_new_note(new_note_data)
    return render(request, 'lp_backend/vendors/client_checking.html', {'user_info': user_data})
