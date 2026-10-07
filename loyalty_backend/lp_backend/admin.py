from django.contrib import admin

from lp_backend.models import Client, Operation, DiscountTier
# Register your models here.

admin.site.register(Client)
admin.site.register(Operation)
admin.site.register(DiscountTier)