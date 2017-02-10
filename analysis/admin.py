from django.contrib import admin

# Register your models here.
from .models import Language

# give language model admin interface
admin.site.register(Language)
