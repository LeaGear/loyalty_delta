from django.contrib import messages
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, redirect

from lp_backend.exceptions import ServiceError
from lp_backend.services import get_client_id_by_param, get_client_data, add_new_note, delete_note, add_new_operation, delete_operation, get_all_client_notes, get_all_client_operations
from lp_backend.web.messages import error_text

@require_GET
def client_loyalty_view(request):
    return render(request, 'lp_backend/vendors/client_checking.html')

@require_GET
def client_page_view(request, client_id):
    try:
        client_info = get_client_data(client_id)
        client_info['notes'] = get_all_client_notes(client_id)
        client_info['operations'] = get_all_client_operations(client_id)
    except ServiceError as e:
        messages.error(request, error_text(e))
        return redirect('client_loyalty_page')

    return render(request, 'lp_backend/vendors/client_checking.html', {'user_info': client_info})


@require_GET
def search_client_view(request):
    client_param = request.GET.get('client-param', '').strip()
    if not client_param:
        return redirect('client_loyalty_page')
    try:
        client_inner_id = get_client_id_by_param(client_param)
        messages.success(request, 'Client found successfully!')
        return redirect('client_page', client_inner_id)
    except ServiceError as e:
        messages.error(request, error_text(e))
        return redirect('client_loyalty_page')

@require_POST
def add_note_view(request, client_id):
    try:
        note_text = request.POST.get('note-text', '').strip()
        add_new_note(client_id, note_text)
        messages.success(request, 'Note added successfully!')
    except ServiceError as e:
        messages.error(request, error_text(e))

    return redirect('client_page', client_id)

@require_POST
def del_note_view(request, client_id, note_id):
    try:
        delete_note(note_id, client_id)
        messages.success(request, 'Note deleted successfully!')
    except ServiceError as e:
        messages.error(request, error_text(e))
    return redirect('client_page', client_id)

@require_POST
def add_operation_view(request, client_id):
    try:
        operation_amount = request.POST.get('oper-amount', '').strip()
        operation_type = request.POST.get('oper-type', '').strip()
        add_new_operation(operation_amount, operation_type, client_id)
        messages.success(request, 'Operation added successfully!')
    except ServiceError as e:
        messages.error(request, error_text(e))
    return redirect('client_page', client_id)

@require_POST
def del_operation_view(request, client_id, operation_id):
    try:
        delete_operation(operation_id, client_id)
        messages.success(request, 'Operation deleted successfully!')
    except ServiceError as e:
        messages.error(request, error_text(e))
    return redirect('client_page', client_id)