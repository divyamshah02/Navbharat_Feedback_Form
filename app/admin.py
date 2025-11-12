from django.contrib import admin
from .models import OTPVerification, UserInfo

# Register your models here.
class AdminOtpVerification(admin.ModelAdmin):
    list_display = ('id', 'mobile', 'otp', 'is_verified', 'created_at', 'expires_at')
    search_fields = ('mobile', 'otp')
    list_filter = ('is_verified', 'created_at', 'expires_at')

class AdminUserInfo(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'email', 'created_at')
    search_fields = ('name', 'mobile', 'email')
    list_filter = ('created_at',)

admin.site.register(OTPVerification, AdminOtpVerification)
admin.site.register(UserInfo, AdminUserInfo)
