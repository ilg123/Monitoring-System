from celery import shared_task
from concurrent.futures import ThreadPoolExecutor
import requests
from .models import Machine, Metric, Incident
from django.utils.timezone import now

@shared_task
def poll_endpoints():
    machines = Machine.objects.all()
    
    def fetch_data(machine):
        try:
            response = requests.get(machine.endpoint_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            Metric.objects.create(
                machine=machine,
                cpu=data['cpu'],
                mem=data['mem'],
                disk=data['disk'],
                uptime=data['uptime']
            )
        except Exception as e:
            print(f"Error fetching data from {machine.name}: {e}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch_data, machines)

@shared_task
def check_incidents():
    from datetime import timedelta
    
    thresholds = {
        'CPU': 85,
        'Mem': 85,
        'Disk': 90,
    }

    for machine in Machine.objects.all():
        for param, threshold in thresholds.items():
            time_window = now() - timedelta(minutes=30 if param != 'Disk' else 120)
            metrics = Metric.objects.filter(
                machine=machine,
                timestamp__gte=time_window,
                **{param.lower() + '__gt': threshold}
            )

            if metrics.exists():
                incident, created = Incident.objects.get_or_create(
                    machine=machine,
                    parameter=param,
                    is_resolved=False,
                    defaults={'start_time': now()}
                )
            else:
                Incident.objects.filter(
                    machine=machine,
                    parameter=param,
                    is_resolved=False
                ).update(is_resolved=True, end_time=now())