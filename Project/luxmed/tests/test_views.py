from django.test import Client, TestCase
from django.urls import reverse, resolve
from ..views import Index, login, logout, error, contact, ValidateUser, AddVisit, DeleteTask, home
from ..forms import LoginForm, VisitForm

#python3 manage.py test luxmed

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.View_Index_url = reverse('Index')
        self.View_login_url = reverse('login')
        self.View_logout_url = reverse('logout')
        self.View_error_url = reverse('error')
        self.View_contact_url = reverse('contact')
        self.View_ValidateUser_url = reverse('ValidateUser')
        self.View_AddVisit_url = reverse('AddVisit')
        self.View_DeleteTask_url = reverse('DeleteTask')


    def testIndexViewGET(self):
        response = self.client.get(self.View_Index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/Index.html')

    def testloginViewGET(self):
        response = self.client.get(self.View_login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/login.html')
    
    def testloginViewPOST(self):
        response = self.client.post(self.View_login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/login.html')

    def testlogoutViewGET(self):
        response = self.client.get(self.View_logout_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/Index.html')

    def testerrorViewGET(self):
        response = self.client.get(self.View_error_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/error.html')

    def testcontactViewGET(self):
        response = self.client.get(self.View_contact_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/contact.html')
    
    def testValidateUserViewGET(self):
        response = self.client.get(self.View_ValidateUser_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/login.html')

    def testValidateUserViewPOST_no_form_submit(self):
        response = self.client.post(self.View_ValidateUser_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/error.html')

    def testValidateUserViewPOST_wrong_form_submit(self):
        form = LoginForm(initial={'username': 'random@random.com', 'userpass': 'randompass'})

        response = self.client.post(self.View_ValidateUser_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'luxmed/error.html')


    def testDeleteTaskViewPOST(self):
        response = self.client.post(self.View_DeleteTask_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/home/')


    def testAddVisitViewGET(self):
        session = self.client.session
        session['username'] = 'random@random.com'
        session['userpass'] = 'randompass'
        session.save()

        response = self.client.get(self.View_AddVisit_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "luxmed/AddVisit.html")

    def testAddVisitViewPOST_without_form(self):
        session = self.client.session
        session['username'] = 'random@random.com'
        session['userpass'] = 'randompass'
        session.save()
        form = VisitForm(initial={'UserEmail': 'random@random.com', 'UserPassword': 'randompass', 'City': '45', 'Service': '5844', 'TimeFrom': '01-01-2019', 'TimeTo': '01-01-2020', 'WhatsappNr': '+48111111111'})


        response = self.client.post(self.View_AddVisit_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "luxmed/error.html")

