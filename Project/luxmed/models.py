from django.db import models
from django.core.validators import RegexValidator
from luxmed.LuxMedAPI.LuxmedAPI import LuxMedConnector
import datetime
from .WhatsApp import SendWhatsApp
from phonenumber_field.modelfields import PhoneNumberField

# SQL MODEL - Table with all LuxMed Services
class LuxMedService(models.Model):
    LuxMedID = models.IntegerField()
    ServiceName = models.CharField(max_length=120)

    def __str__(self):
        return self.ServiceName

    def __unicode__(self):
        return self.LuxMedID

# SQL MODEL - Table with all LuxMed Locations
class LuxMedLocation(models.Model):
    LuxMedID = models.IntegerField()
    LocationName = models.CharField(max_length=120)

    def __str__(self):
        return self.LocationName

    def __unicode__(self):
        return self.LocationName


# SQL MODEL - Table with all Tasks (Visits to look for)
class MyTask(models.Model):

    # Define the parameters of the Task Class
    UserEmail = models.CharField(max_length=120)
    UserPassword = models.CharField(max_length=120)
    City = models.ForeignKey(LuxMedLocation, on_delete=models.CASCADE)
    Service = models.ForeignKey(LuxMedService, on_delete=models.CASCADE)
    TimeFrom = models.TimeField()
    TimeTo = models.TimeField()
    VisitDate = models.DateTimeField(blank=True, null=True)
    LastCheck = models.DateTimeField(blank=True, null=True)
    WhatsappNr = PhoneNumberField(null=False, blank=False, help_text='Notification phone number')
   
    #METHOD to refresh the task data - Check if there is a new visit on LuxMED
    def GetNewVisit(self):

        #Create LuxMed connector class and login to LuxMed portal
        LuxMedConn = LuxMedConnector()
        LuxMedConn.LUXemail = self.UserEmail
        LuxMedConn.LUXpassword = self.UserPassword
        LuxMedConn._createSession()
        LuxMedConn._logIn() 

        #Check if login succesful
        if LuxMedConn.LoginStatus==True:

            #Pass the City ID and Service ID to look for in LuxMed portal
            LuxMedConn.Find_Location = self.City.LuxMedID
            LuxMedConn.Find_Service = self.Service.LuxMedID

            #Get all visits for service and city from luxmed portal for next 90 days
            ImportedVisitList = LuxMedConn._getAppointments()

            # Variable to Validate if the visit was found
            VisitFound = False

            #Loop through all imported visits from LuxMed service
            for VisitObject in ImportedVisitList:

                AppointmentDate = VisitObject.get('AppointmentDate') # Get the visit date
                DoctorName = VisitObject.get('DoctorName') # Get the Doctor Name
                ClinicPublicName = VisitObject.get('ClinicPublicName') # Get the City location name
                AppointmentServiceName = self.Service.ServiceName # Get the Service name

                # Extract the date value from string - Imported visit data
                AppointmentDate = AppointmentDate[len(AppointmentDate)-16:len(AppointmentDate)] 
                
                # Extract the time value from a string - Imported visit data
                AppointmentDate_Time = datetime.datetime.strptime((AppointmentDate[len(AppointmentDate)-5:len(AppointmentDate)]), '%H:%M')

                # Prepare old and new Visits date times to compare 
                DateCheck_New = datetime.datetime.strptime(AppointmentDate , '%d-%m-%Y %H:%M')
                DateCheck_Old = self.VisitDate

                
                # Compare:
                if self.VisitDate is None: # If the visit is new - Import first date
                    self.VisitDate=DateCheck_New
                    VisitFound = True
                    
                    # Send WhatsApp message
                    SendWhatsApp(str(DoctorName), str(AppointmentDate), str(ClinicPublicName), str(AppointmentServiceName), self.WhatsappNr.as_e164)
                   # SendWhatsApp(str(DoctorName), str(AppointmentDate), str(ClinicPublicName), str(AppointmentServiceName), str(self.WhatsappNr))
                    
                else: # Visit already found - Check if there is a new visit
                    if (AppointmentDate_Time.time() > self.TimeFrom) and (AppointmentDate_Time.time() < self.TimeTo) and (DateCheck_New.replace(tzinfo=None) < DateCheck_Old.replace(tzinfo=None)) and VisitFound == False:
                        self.VisitDate=DateCheck_New
                        VisitFound = True

                        # Send WhatsApp message
                        SendWhatsApp(str(DoctorName), str(AppointmentDate), str(ClinicPublicName), str(AppointmentServiceName), self.WhatsappNr.as_e164)
                       # SendWhatsApp(str(DoctorName), str(AppointmentDate), str(ClinicPublicName), str(AppointmentServiceName), str(self.WhatsappNr))
                                   
               
               # Update the last check date for task
                self.LastCheck = datetime.datetime.now()

            return True # Login to LuxMed portal succesful
        else:
            return False # Login to LuxMed portal failed




