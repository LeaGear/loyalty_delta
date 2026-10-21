from django.urls import path

from lp_backend.web.views import base_view, client_page_view, search_client_view, add_note_view, del_note_view, add_transaction_view, del_transaction_view

urlpatterns =[
    path('base/',base_view, name='Base_view'),
    path('client/<int:client_id>', client_page_view, name='client_page'),
    path('search_client/', search_client_view, name='search_client'),
    path('client/<int:client_id>/add_note/', add_note_view, name='add_note'),
    path('client/<int:client_id>/del_note/<int:note_id>', del_note_view, name='del_note'),
    path('client/<int:client_id>/add_transaction/', add_transaction_view, name='add_transaction'),
    path('client/<int:client_id>/del_transaction/<int:transaction_id>', del_transaction_view, name='del_transaction'),
]