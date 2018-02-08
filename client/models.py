from django.db import models

# Create your models here.
class Client(models.Model):
    client_uuid = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    resource_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)

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
    due_date = models.DateTimeField()
    job_task_time_difference = models.CharField(max_length=80)
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
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    system_type = models.CharField(max_length=2, choices=SYSTEM_TYPES)
    contracted = models.CharField(max_length=1, choices=YES_NO)
    contract_date = models.DateField()
    install_date = models.DateField()
    maintenance_interval = models.CharField(max_length=1, choices=INTERVAL)
    monitoring_type = models.CharField(max_length=1, choices=MONITORING_TYPE)
    monitoring_acct_num = models.CharField(max_length=80)
    maintenance_form_setup = models.CharField(max_length=1, choices=YES_NO)
    urn_intruder = models.CharField(max_length=80)
    urn_pa = models.CharField(max_length=80)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.system_type
