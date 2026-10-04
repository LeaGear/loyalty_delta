from django.contrib import admin
from django.contrib.auth.models import User

from lp_backend.models import Client, Operation
# Register your models here.

admin.site.register(Client)
admin.site.register(Operation)
