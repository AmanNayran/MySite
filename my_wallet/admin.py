from django.contrib import admin

# Register your models here.
from .models import Stock, Transaction

admin.site.register(Stock)
admin.site.register(Transaction)
