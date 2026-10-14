
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render

# TODO: TEST
USER_INFO_TEST = {
    'id': 12551512,
    'name': 'Duha',
    'code': 125135561,
    'number': '+123142352352'
}

@require_GET
def base_view(request):
    return render(request, 'lp_backend/vendors/client_checking.html', {'user_info': USER_INFO_TEST})