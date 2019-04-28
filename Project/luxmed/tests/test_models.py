from django.test import TestCase
from ..models import MyTask, LuxMedLocation, LuxMedService
from ..LuxMedAPI.LuxmedAPI import LuxMedConnector
from datetime import date, datetime

#python3 manage.py test luxmed

class TestModels(TestCase):

    def setUp(self):
        self.LuxMedService1 = LuxMedService.objects.create(LuxMedID=9898, ServiceName='Test Service')
        self.LuxMedLocation1 = LuxMedLocation.objects.create(LuxMedID=99, LocationName='Test Location')



    def testLuxMedServiceDisplayName(self):
        self.assertEquals(self.LuxMedService1.__str__(), 'Test Service') 
        self.LuxMedService1.save()

    def testLuxMedLocationDisplayName(self):
        self.assertEquals(self.LuxMedLocation1.__str__(), 'Test Location') 
        self.LuxMedLocation1.save()