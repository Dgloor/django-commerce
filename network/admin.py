from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import User, Post

class CustomUserAdmin(UserAdmin):
    filter_horizontal = ("following",)
    fieldsets = UserAdmin.fieldsets + (
        ("Following", {"fields": ("following",)}),
    )

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes",)
    list_display = ("id", "content", "timestamp", "creator")


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
