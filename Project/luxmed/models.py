from django.db import models
from django.core.validators import RegexValidator
from luxmed.LuxMedAPI.LuxmedAPI import LuxMedSniper
import datetime
from datetime import date
from .WhatsApp import SendWhatsApp

class LuxMedService(models.Model):
    LuxMedID = models.IntegerField()
    ServiceName = models.CharField(max_length=120)

    def __str__(self):
        return self.ServiceName

    def __unicode__(self):
        return self.LuxMedID

class LuxMedLocation(models.Model):
    LuxMedID = models.IntegerField()
    LocationName = models.CharField(max_length=120)

    def __str__(self):
        return self.LocationName

    def __unicode__(self):
        return self.LocationName



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

    def GetNewVisit(self):
        LuxMedConn = LuxMedSniper()
        LuxMedConn.LUXemail = self.UserEmail
        LuxMedConn.LUXpassword = self.UserPassword
        LuxMedConn._createSession()
        LuxMedConn._logIn()
        if LuxMedConn.LoginStatus==True:

            LuxMedConn.Find_Location = self.City.LuxMedID
            LuxMedConn.Find_Service = self.Service.LuxMedID

            ImportedVisitList=LuxMedConn._getAppointments()
            checker = True

            for a in ImportedVisitList:
                test = a.get('AppointmentDate')
                testt = a.get('DoctorName')
                testtt = a.get('ClinicPublicName')
                testttt = self.Service.ServiceName

                test1 = test[len(test)-16:len(test)]
                Timeer = datetime.datetime.strptime((test[len(test)-5:len(test)]), '%H:%M')

                datecheck1 = datetime.datetime.strptime(test1 , '%d-%m-%Y %H:%M')
                datecheck2 = self.VisitDate

                
                if self.VisitDate is None:
                    FinalDate = datetime.datetime.strptime(test1 , '%d-%m-%Y %H:%M')
                    self.VisitDate=FinalDate
                    checker = False

                    SendWhatsApp(str(testt), str(test), str(testtt), str(testttt))
                    
                else: 
                    if (Timeer.time() > self.TimeFrom) and (Timeer.time() < self.TimeTo) and (datecheck1.replace(tzinfo=None) < datecheck2.replace(tzinfo=None)) and checker == True:
                        print(datecheck1)
                        print(datecheck2)

                        FinalDate = datetime.datetime.strptime(test1 , '%d-%m-%Y %H:%M')
                        self.VisitDate=FinalDate
                        checker = False

                        SendWhatsApp(str(testt), str(test), str(testtt), str(testttt))

                self.LastCheck = datetime.datetime.now()

            return True
        else:
            return False




