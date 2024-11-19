from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django import forms
from django.utils.html import mark_safe

from applications.website.models import Customer, Product, Category, OrderItem, Order, CartItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'fullname', 'email')
    search_fields = ('username', 'fullname', 'email')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    price = forms.DecimalField(widget=forms.NumberInput(attrs={'style': 'width: 200px;'}))
    retail_price = forms.DecimalField(widget=forms.NumberInput(attrs={'style': 'width: 200px;'}))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_status', 'created_at', 'total_price', 'view_order_items')
    list_filter = ('order_status', 'created_at')
    search_fields = ('id', 'customer__fullname')
    inlines = [OrderItemInline]
    readonly_fields = ('total_price', 'created_at')

    def view_order_items(self, obj):
        items = obj.orderitem_set.all()
        return ", ".join([f"{item.product.name} (x{item.quantity})" for item in items])
    view_order_items.short_description = 'Chi tiết đơn hàng'

