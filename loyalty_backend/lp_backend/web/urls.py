from django.urls import path

from lp_backend.web.views import client_loyalty_view, client_page_view, search_client_view, add_note_view, del_note_view, add_operation_view, del_operation_view, login_view, logout_view

urlpatterns =[
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('client_loyalty/',client_loyalty_view, name='client_loyalty_page'),
    path('client/<int:client_id>', client_page_view, name='client_page'),
    path('search_client/', search_client_view, name='search_client'),
    path('client/<int:client_id>/add_note/', add_note_view, name='add_note'),
    path('client/<int:client_id>/del_note/<int:note_id>', del_note_view, name='del_note'),
    path('client/<int:client_id>/add_operation/', add_operation_view, name='add_operation'),
    path('client/<int:client_id>/del_operation/<int:operation_id>', del_operation_view, name='del_operation'),
]