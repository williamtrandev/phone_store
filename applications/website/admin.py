from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.html import mark_safe

from applications.website.models import Customer, Product, Category


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'fullname', 'email')
    search_fields = ('username', 'fullname', 'email')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_phone', 'price', 'retail_price', 'image_thumbnail']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'is_phone']
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'is_phone', 'color', 'ram', 'rom', 'price', 'retail_price', 'image', 'detail')
        }),
    )
    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "No image"

    image_thumbnail.short_description = 'Image'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass