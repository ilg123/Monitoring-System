from django.shortcuts import render
from django.http import JsonResponse

from .models import Incident


def api_incidents(request):
    incidents = Incident.objects.filter(is_resolved=False)
    data = {
        'incidents': [
            {
                'machine': incident.machine.name,
                'parameter': incident.parameter,
                'start_time': incident.start_time.isoformat(),
                'is_resolved': incident.is_resolved
            }
            for incident in incidents
        ]
    }
    return JsonResponse(data)