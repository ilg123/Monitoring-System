from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=100)
    endpoint_url = models.URLField()
    
    def __str__(self):
        return self.name

class Metric(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    cpu = models.DecimalField(max_digits=5, decimal_places=2)
    mem = models.DecimalField(max_digits=5, decimal_places=2)
    disk = models.DecimalField(max_digits=5, decimal_places=2)
    uptime = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.machine.name} at {self.timestamp}"

class Incident(models.Model):
    PARAMETER_CHOICES = [
        ('CPU', 'CPU'),
        ('Mem', 'Memory'),
        ('Disk', 'Disk'),
    ]
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=4, choices=PARAMETER_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.machine.name} - {self.parameter} at {self.start_time}"