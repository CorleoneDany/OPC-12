from django.contrib import admin
from .models import Client, Contract, ContractStatus, Event

# Register your models here.

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(ContractStatus)
admin.site.register(Event)
