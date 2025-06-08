from django.contrib import admin

from users.models import User, EmailConfirmation

admin.site.register(User)

# admin.site.register(EmailConfirmation)

@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    list_filter = ('user',)