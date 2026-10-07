from django.urls import path

from lp_backend.api.views import registration_user_view, check_user_status_view, get_user_loyalty_code_view, get_user_data_view

urlpatterns = [
    path('registration/', registration_user_view, name='registration'),
    path('client_status/<int:user_id>', check_user_status_view, name='user_status'),
    path('loyalty_code/<int:user_id>', get_user_loyalty_code_view, name='get_user_loyalty_code'),
    path('user_data/<int:user_id>', get_user_data_view, name='user_data'),
]