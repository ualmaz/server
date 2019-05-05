from django.contrib import admin
from .models import Area, Country, Post, User, Profile, Report


admin.site.register(User)
admin.site.register(Area)
admin.site.register(Country)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Report)
