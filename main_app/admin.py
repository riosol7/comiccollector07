from django.contrib import admin

# Register your models here.
from .models import Comic, Log, Photo, Profile

admin.site.register(Comic)
admin.site.register(Log)
admin.site.register(Photo)
admin.site.register(Profile)
