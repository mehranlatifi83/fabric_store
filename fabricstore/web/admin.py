from django.contrib import admin
from .models import Fabric, MyUser
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ['phone', 'first_name', 'last_name', 'is_admin']
    search_fields = ['phone', 'first_name', 'last_name']
    readonly_fields = ['phone']
    ordering = ['phone']
    # حذف فیلدهای ناسازگار در fieldsets و add_fieldsets
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_admin'),
        }),
    )

    # حذف فیلدهای ناسازگار در list_filter و filter_horizontal
    list_filter = ('is_admin', 'is_active')
    filter_horizontal = ()
    exclude = ('username', 'groups', 'user_permissions', 'is_staff', 'is_superuser')
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Fabric)
