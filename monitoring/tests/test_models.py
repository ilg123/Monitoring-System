import pytest
from monitor.models import Machine, Metric, Incident
from django.utils import timezone
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_machine_creation(create_machine):
    assert create_machine.name == 'Test Model'
    assert create_machine.endpoint_url == 'http://example.com'
    assert str(create_machine) == 'Test Model'

@pytest.mark.django_db
def test_metric_creation(create_metric, create_machine):
    assert create_metric.machine == create_machine
    assert create_metric.cpu == 50.00
    assert create_metric.mem == 50.00
    assert create_metric.disk == 50.00
    assert create_metric.uptime == 50
    assert str(create_metric) == f'{create_machine.name} at {create_metric.timestamp}'

@pytest.mark.django_db
def test_metric_foreignkey_delete(create_machine, create_metric):
    assert Metric.objects.count() == 1
    create_machine.delete()
    assert Metric.objects.count() == 0

@pytest.mark.django_db
def test_incident_creation_CPU(create_machine, create_incident):
    assert create_incident.machine == create_machine
    assert create_incident.parameter == 'CPU'
    assert create_incident.end_time is None
    assert create_incident.is_resolved is False
    assert str(create_incident) == f'{create_machine.name} - CPU at {create_incident.start_time}'

@pytest.mark.django_db
def test_incident_parameter_invalid_choices(create_machine, create_incident):
    with pytest.raises(ValidationError):
        incident = Incident(
            machine =create_machine,
            parameter='InvalidParam',
            start_time=timezone.now(),
            is_resolved=False
        )
        incident.full_clean()
        create_incident.full_clean()
    
@pytest.mark.django_db
def test_incident_resolution(create_incident):
    create_incident.end_time = timezone.now()
    create_incident.is_resolved = True

    assert create_incident.end_time is not None
    assert create_incident.is_resolved is True