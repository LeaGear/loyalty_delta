from django.urls import path

from lp_backend.views import test_view, registration_user_view

urlpatterns = [
    path('test/', test_view, name='test'),
    path('registration/', registration_user_view, name='registration'),
]