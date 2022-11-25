from django.contrib import admin

# Register your models here.
from stripe_app.models import Item, Order, Discount


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass
