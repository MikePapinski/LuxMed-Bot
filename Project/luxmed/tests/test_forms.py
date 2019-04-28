from django.test import TestCase
from ..forms import LoginForm, DeleteTaskForm, VisitForm
from ..models import  LuxMedLocation, LuxMedService

#python3 manage.py test luxmed

class TestForms(TestCase):

    def testLoginForm_valid_data(self):
        form = LoginForm(data={'your_name':'sample@sample.com', 'your_pass':'samplepass'})
        self.assertTrue(form.is_valid())


    def testLoginForm_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

    def testVisitForm_valid_data(self):
        LuxMedLocation.objects.create(LuxMedID=99, LocationName='Test Location')
        LuxMedService.objects.create(LuxMedID=9898, ServiceName='Test Service')
        RandomCity = LuxMedLocation.objects.get(LuxMedID=99, LocationName='Test Location').pk
        RandomService = LuxMedService.objects.get(LuxMedID=9898, ServiceName='Test Service').pk

        form = VisitForm(data={'UserEmail':'sample@sample.com', 'UserPassword':'sample123', 'City':RandomCity, 'Service':RandomService,'TimeFrom':'15:30','TimeTo':'20:00','WhatsappNr':'+48884988538'})
        self.assertTrue(form.is_valid())


    def testVisitForm_no_data(self):
        form = VisitForm(data={})
        self.assertFalse(form.is_valid())

    def testDeleteTaskForm_valid_data(self):
        form = DeleteTaskForm(data={'DeleteTaskID':999})
        self.assertTrue(form.is_valid())


    def testDeleteTaskForm_no_data(self):
        form = DeleteTaskForm(data={})
        self.assertFalse(form.is_valid())