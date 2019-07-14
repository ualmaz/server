from django.contrib import admin
from .models import Area, Country, Post, User, Profile, Report



admin.site.register(Area)

class CustomCountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'access_challenge')
admin.site.register(Country, CustomCountryAdmin)

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Report)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name', 'is_active')



admin.site.register(User, CustomUserAdmin)

admin.site.site_header = 'Welcome World Changer!'

