from django.urls import path

from lp_backend.web.views import base_view, search_client_view, add_note_view, add_transaction_view

urlpatterns =[
    path('base/',base_view, name='Base_view'),
    path('search_client/', search_client_view, name='search_client'),
    path('add_note/', add_note_view, name='add_note'),
    path('add_transaction/', add_transaction_view, name='add_transaction'),
]