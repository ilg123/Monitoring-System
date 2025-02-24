from django.contrib import admin
from .models import Machine, Metric, Incident

admin.site.register(Machine)
admin.site.register(Metric)
admin.site.register(Incident)
# Register your models here.
