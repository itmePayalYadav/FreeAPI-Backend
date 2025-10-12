from django.contrib import admin
from .models import (
    Category, Endpoint, Example, ResponseModel,
    Subscription, Usage, Media
)

# =========================================================
# Category Admin
# =========================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('name',)
    list_filter = ('created_at', 'updated_at')


# =========================================================
# Example Inline for Endpoint
# =========================================================
class ExampleInline(admin.TabularInline):
    model = Example
    extra = 1
    fields = ('language', 'request_type', 'code_snippet')
    readonly_fields = ()
    show_change_link = True


# =========================================================
# Response Inline for Endpoint
# =========================================================
class ResponseInline(admin.TabularInline):
    model = ResponseModel
    extra = 1
    fields = ('status_code', 'media_type', 'headers', 'body')
    readonly_fields = ()
    show_change_link = True


# =========================================================
# Media Inline for Endpoint
# =========================================================
class MediaInline(admin.TabularInline):
    model = Media
    extra = 1
    fields = ('file', 'description')
    readonly_fields = ()
    show_change_link = True


# =========================================================
# Endpoint Admin
# =========================================================
@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'method', 'url', 'category', 'is_premium', 'created_at')
    search_fields = ('name', 'slug', 'url', 'method')
    list_filter = ('method', 'category', 'is_premium', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('name',)
    inlines = [ExampleInline, ResponseInline, MediaInline]


# =========================================================
# Example Admin
# =========================================================
@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('api', 'language', 'request_type', 'created_at')
    search_fields = ('api__name', 'language', 'request_type')
    list_filter = ('language', 'request_type', 'created_at')


# =========================================================
# ResponseModel Admin
# =========================================================
@admin.register(ResponseModel)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('api', 'status_code', 'media_type', 'created_at')
    search_fields = ('api__name', 'status_code', 'media_type')
    list_filter = ('status_code', 'media_type', 'created_at')


# =========================================================
# Subscription Admin
# =========================================================
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'api', 'accessed_at', 'usage_count')
    search_fields = ('user__username', 'api__name')
    list_filter = ('accessed_at',)
    readonly_fields = ('usage_count', 'accessed_at')


# =========================================================
# Usage Admin
# =========================================================
@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'method', 'status_code', 'request_time')
    search_fields = ('subscription__user__username', 'subscription__api__name', 'method')
    list_filter = ('method', 'status_code', 'request_time')


# =========================================================
# Media Admin
# =========================================================
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('api', 'file', 'description', 'created_at')
    search_fields = ('api__name', 'description')
    list_filter = ('created_at',)
