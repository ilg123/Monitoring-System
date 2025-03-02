import pytest
from unittest.mock import patch, MagicMock
from django.utils.timezone import now, timedelta
from monitor.models import Machine, Metric, Incident
from monitor.tasks import poll_endpoints, check_incidents

@pytest.mark.django_db(transaction=True)
def test_poll_endpoints():
    machine = Machine.objects.create(name='Test Model', endpoint_url='http://example.com')
    mock_response = MagicMock()
    mock_response.json.return_value = {'cpu': 75.0, 'mem': 60.0, 'disk': 80.0, 'uptime': 3600}
    
    with patch('requests.get', return_value=mock_response):
        poll_endpoints()
    
    metrics = Metric.objects.filter(machine=machine)
    assert metrics.count() == 1
    assert metrics.first().cpu == 75.0

@pytest.mark.django_db(transaction=True)
def test_check_incidents():
    machine = Machine.objects.create(name='Test Model', endpoint_url='http://example.com')
    Metric.objects.bulk_create([
        Metric(machine=machine, cpu=90.0, mem=70.0, disk=50.0, uptime=3600, timestamp=now() - timedelta(minutes=15)),
        Metric(machine=machine, cpu=92.0, mem=65.0, disk=55.0, uptime=3700, timestamp=now())
    ])
    
    check_incidents()
    
    incidents = Incident.objects.filter(machine=machine, parameter='CPU', is_resolved=False)
    assert incidents.count() == 1
    assert incidents.first().parameter == 'CPU'