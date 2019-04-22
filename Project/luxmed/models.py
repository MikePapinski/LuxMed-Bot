from django.db import models
from django.core.validators import RegexValidator

class LuxMedService(models.Model):
    LuxMedID = models.IntegerField()
    ServiceName = models.CharField(max_length=120)

    def __str__(self):
        return u'%s %s' % (self.LuxMedID, self.ServiceName)

    def __unicode__(self):
        return u'%s %s' % (self.LuxMedID,  self.ServiceName)

class LuxMedLocation(models.Model):
    LuxMedID = models.IntegerField()
    LocationName = models.CharField(max_length=120)

    def __str__(self):
        return u'%s %s' % (self.LuxMedID, self.LocationName)

    def __unicode__(self):
        return u'%s %s' % (self.LuxMedID, self.LocationName)



class MyTask(models.Model):
    UserEmail = models.CharField(max_length=120)
    UserPassword = models.CharField(max_length=120)
    City = models.ForeignKey(LuxMedLocation, on_delete=models.CASCADE)
    Service = models.ForeignKey(LuxMedService, on_delete=models.CASCADE)
    TimeFrom = models.TimeField()
    TimeTo = models.TimeField()
    VisitDate = models.DateTimeField(blank=True, null=True)
    LastCheck = models.DateTimeField(blank=True, null=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    WhatsappNr = models.CharField(validators=[phone_regex], max_length=17) # validators should be a list

