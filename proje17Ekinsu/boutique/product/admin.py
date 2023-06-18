from django.contrib import admin
from .models import *
class BasketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'product', 'number', 'totalPrice', 'payment')
    list_filter = ('owner', 'payment')
# Register your models here.
admin.site.register(Product)
admin.site.register(Kategori)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Payment)
