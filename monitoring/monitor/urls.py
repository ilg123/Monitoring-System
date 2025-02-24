from django.urls import path
from .views import api_incidents

urlpatterns = [
    path('incidents/', api_incidents, name='incident'),
]