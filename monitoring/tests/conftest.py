import pytest
from monitor.models import Machine, Metric, Incident
from django.utils import timezone

@pytest.fixture
def create_machine():
    return Machine.objects.create(
        name='Test Model',
        endpoint_url='http://example.com'
    )

@pytest.fixture
def create_metric(create_machine):
    return Metric.objects.create(
        machine=create_machine,
        cpu=50.00,
        mem=50.00,
        disk=50.00,
        uptime=50,
        timestamp=timezone.now(),
    )

@pytest.fixture
def create_incident(create_machine):
    return Incident.objects.create(
        machine=create_machine,
        parameter='CPU',
        start_time=timezone.now(),
        end_time=None,
        is_resolved=False
    )
