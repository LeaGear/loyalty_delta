
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render


@require_GET
def base_view(request):
    return render(request, 'lp_backend/vendors/client_checking.html')