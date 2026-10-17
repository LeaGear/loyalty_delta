from django.urls import path

from lp_backend.web.views import base_view, search_client_view

urlpatterns =[
    path('base/',base_view, name='Base_view'),
    path('search_client/', search_client_view, name='search_client'),
]