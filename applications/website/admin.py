from django.contrib import admin
from django.contrib.auth.hashers import make_password

from applications.website.models import Staff, Customer


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'fullname', 'email')
    search_fields = ('username', 'fullname', 'email')
    exclude = ('password',)

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

