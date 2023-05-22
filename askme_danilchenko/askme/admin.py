from django.contrib import admin
from . import models

admin.site.register(models.Questions)
admin.site.register(models.Answers)
admin.site.register(models.Tags)
admin.site.register(models.Profile)
