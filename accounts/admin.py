from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, UserDetail
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('id','email', 'org_admin', 'is_verified', 'is_suspended', 'is_staff', 'user_detail')
    list_filter = ('is_staff', 'is_suspended', 'org_admin')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login','email_verified_at')
    fieldsets = (
                 (None, {'fields':('email', 'password')}),
                 ('Account Settings', {'fields': ('is_verified',)}),
                 ('Account Activity', {'fields': ('date_joined', 'email_verified_at', 'last_forgeted_at', 'last_login')}),
                 ('Permissions', {'fields':('is_staff', 'is_active', 'is_suspended', 'org_admin')}))

    add_fieldsets = (
            (
            None, {
            'classes':('wide',), 
            'fields':('email', 'password1', 'password2', 'is_suspended', 'org_admin', 'is_staff', 'is_active')
            }),
        )

    ordering = ('-date_joined',)


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'phone', 'profile_pic']


admin.site.register(User, CustomUserAdmin)

admin.site.site_title = "Alumni Connect Admin"
admin.site.site_header = "Alumni Connect Administration"
admin.site.index_title = "Administration"