from django.contrib import admin

from lp_backend.models import Client, Operation, DiscountTier, ClientNote
# Register your models here.

admin.site.register(Client)
admin.site.register(Operation)
admin.site.register(DiscountTier)
admin.site.register(ClientNote)