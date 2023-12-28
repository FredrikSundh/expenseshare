from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Expense)
admin.site.register(User)
admin.site.register(PaymentInformation)