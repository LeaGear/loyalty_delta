from django.urls import path

from lp_backend.views import test_view, registration_user_view, check_user_status_view

urlpatterns = [
    path('test/', test_view, name='test'),
    path('registration/', registration_user_view, name='registration'),
    path('client_status/<int:user_id>', check_user_status_view, name='user_status'),
]