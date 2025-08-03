from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "Профиль пользователя"
    verbose_name_plural = "Профили пользователей"
    fields = ['department', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'get_department', 'is_staff']
    list_filter = ['is_staff']
    search_fields = ['username', 'email', 'userprofile__department']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    def get_department(self, obj):
        return obj.userprofile.department or 'Без отдела'
    get_department.short_description = 'Отдел'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'created_at', 'updated_at']
    list_filter = ['department']
    search_fields = ['user__username', 'department']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'department', 'created_at', 'updated_at']
