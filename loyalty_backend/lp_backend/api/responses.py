from django.http import JsonResponse


def ok(detail='', data=None, status_code=200):
    return JsonResponse({
        'status': 'success',
        'detail': detail,
        'data': data
    }, status=status_code)

def fail(detail='', status_code=400):
    return JsonResponse({
        'status': 'error',
        'detail': detail,
        'data': None
    }, status=status_code)