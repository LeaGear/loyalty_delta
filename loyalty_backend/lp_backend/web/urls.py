from django.urls import path

from lp_backend.services import *
from lp_backend.web.views import base_view
urlpatterns =[
    path('base/',base_view, name='Base_view'),
]