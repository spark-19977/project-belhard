import datetime

from django.contrib import admin
from django.utils.text import slugify

from . import models
# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['name', 'slug']
    # prepopulated_fields = { 'slug': ['name']}

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name, allow_unicode=True)
        obj.save()


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['slug', 'creator']
    list_display = ['name', 'category', 'creator']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        obj.slug = slugify(obj.name + f'{datetime.datetime.now().timestamp()}', allow_unicode=True)
        obj.save()
