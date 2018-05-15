from django.db import models

# Create your models here.
class Client(models.Model):
    client_uuid = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    resource_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Job(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    job_uuid = models.CharField(max_length=80, unique=True)
    job_category = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_uuid

class Task(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    task_uuid = models.CharField(max_length=80, unique=True)
    related_object_uuid = models.CharField(max_length=80, unique=False)
    due_date = models.DateField()
    job_task_time_difference = models.DecimalField(max_digits=5, decimal_places=2)
    completed_date = models.DateTimeField()

    def __str__(self):
        return self.task_uuid

class System(models.Model):
    SYSTEM_TYPES = (
        ('AC', 'Access Control'),
        ('AL', 'Alarm'),
        ('CT', 'CCTV'),
        ('DE', 'Door Entry'),
        ('EL', 'Emergency Lights'),
        ('FA', 'Fire Alarm'),
        ('FE', 'Fire Extinguisher'),
        ('KE', 'Key Holding'),
        ('NC', 'Nurse Call'),
        ('R', 'Refuge'),
        ('M', 'Miscellaneous'),
    )
    YES_NO = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    INTERVAL = (
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
        ('H', 'Half yearly'),
        ('T', 'Tri-yearly'),
        ('Q', 'Quarterly'),
    )
    MONITORING_TYPE = (
        ('A', 'Audible'),
        ('M', 'Monitored'),
        ('D', 'Dualcom'),
        ('DI', 'Digi'),
        ('DIP', 'Digi-Plus'),
        ('DIA', 'Digi-Air'),
        ('RC', 'Redcare Classic'),
        ('RS', 'Redcare SEcure'),
        ('N', 'None'),
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    system_type = models.CharField(max_length=2, choices=SYSTEM_TYPES, blank=True, null=True)
    contracted = models.CharField(max_length=1, choices=YES_NO, blank=True, null=True)
    contract_date = models.DateField(blank=True, null=True)
    install_date = models.DateField(blank=True, null=True)
    maintenance_interval = models.CharField(max_length=1, choices=INTERVAL, blank=True, null=True)
    monitoring_type = models.CharField(max_length=3, choices=MONITORING_TYPE, blank=True, null=True)
    monitoring_acct_num = models.CharField(max_length=80, blank=True, null=True)
    system_price_ex_vat = models.DecimalField(max_digits=6, decimal_places=2)
    system_monitoring_cost = models.DecimalField(max_digits=6, decimal_places=2)
    urn_intruder = models.CharField(max_length=80, blank=True, null=True)
    urn_pa = models.CharField(max_length=80, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['client']

    def __str__(self):
        return self.system_type
