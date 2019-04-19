from django.db import models

class MyTask(models.Model):
    UserEmail = models.CharField(max_length=120)
    UserPassword = models.CharField(max_length=120)
    City = models.CharField(max_length=120)
    Service = models.CharField(max_length = 60)
    TimeFrom = models.DateTimeField(blank=True)
    TimeTo = models.DateTimeField(blank=True)
    VisitDate = models.DateTimeField(blank=True)
    LastCheck = models.DateTimeField(blank=True)
    WhatsappNr = models.CharField(max_length=11)
