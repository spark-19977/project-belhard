from django.contrib import admin
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    raw_id_fields = ['product']

# Register your models here.
@admin.register(models.UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone',
                    'address', 'postal_code', 'paid', 'status',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated', 'status']
    inlines = [OrderItemInline]
    search_fields = ['phone', 'postal_code']
    list_editable = ['status']


@admin.register(models.UserData)
class UserDataAdmin(admin.ModelAdmin):
    ...


# @admin.register(models.OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     ...
