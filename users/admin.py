from django.contrib import admin

from users.models import User, EmailConfirmation

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_verified', 'is_active', 'is_staff', 'id')
    search_fields = ('email',)


# admin.site.register(EmailConfirmation)

@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    list_filter = ('user',)