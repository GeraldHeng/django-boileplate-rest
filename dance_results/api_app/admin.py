from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Employee)
admin.site.register(models.Adjudicator)
admin.site.register(models.Event)
admin.site.register(models.Competition)
admin.site.register(models.Dance)
