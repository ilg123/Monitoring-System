import pytest
from django.urls import reverse
from django.utils import timezone
from monitor.views import api_incidents  
from monitor.models import Incident
from django.http import JsonResponse

@pytest.mark.django_db
def test_api_incidents_incidents(create_incident, client):
    response = client.get(reverse('incident'))
    assert response.status_code == 200
    data = response.json()
    assert len(data['incidents']) == 1

@pytest.mark.django_db
def test_api_incidents_no_incidents(create_machine, client):
    incident = Incident.objects.create(
        machine=create_machine,
        parameter='CPU',
        start_time=timezone.now(),
        is_resolved=True
    )
    response = client.get(reverse('incident'))
    assert response.status_code == 200
    data = response.json()
    assert len(data['incidents']) == 0