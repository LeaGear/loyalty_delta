
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, redirect

from lp_backend.services import get_client_id_by_param, get_client_data, add_new_note, delete_note, add_new_transaction, delete_transaction, get_all_client_notes, get_all_client_transactions

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
def client_page_view(request, client_id):
    client_info = get_client_data(client_id)
    client_info['notes'] = get_all_client_notes(client_id)
    client_info['transactions'] = get_all_client_transactions(client_id)
    print(client_info)
    return render(request, 'lp_backend/vendors/client_checking.html', {'user_info': client_info})

@require_GET
def search_client_view(request):
    search_data = request.GET.dict()
    print(search_data)
    client_param = search_data.get('client-param').strip()
    client_inner_id = get_client_id_by_param(client_param)
    return redirect('client_page', client_inner_id)

@require_POST
def add_note_view(request, client_id):
    new_note_data = request.POST.dict()
    note_text = new_note_data.get('note-text').strip()
    add_new_note(client_id, note_text)
    return redirect('client_page', client_id)

@require_POST
def del_note_view(request, client_id, note_id):
    delete_note(note_id, client_id)
    return redirect('client_page', client_id)


@require_POST
def add_transaction_view(request, client_id):
    new_transaction_data = request.POST.dict()
    transaction_amount = new_transaction_data.get('trans-amount').strip()
    transaction_type = new_transaction_data.get('trans-type').strip()
    add_new_transaction(transaction_amount, transaction_type, client_id)
    return redirect('client_page', client_id)

def del_transaction_view(request, client_id, transaction_id):
    delete_transaction(transaction_id, client_id)
    return redirect('client_page', client_id)