import unittest
from django.urls import reverse, resolve
from ..views import Index, login, logout, error, contact, ValidateUser, AddVisit, DeleteTask, home

#python3 manage.py test luxmed

class TestUrls(unittest.TestCase):

    def test_Index_url_is_resolved(self):
        url = reverse('Index')
        self.assertEquals(resolve(url).func, Index)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)
    
    def test_error_url_is_resolved(self):
        url = reverse('error')
        self.assertEquals(resolve(url).func, error)

    def test_contact_url_is_resolved(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_ValidateUser_url_is_resolved(self):
        url = reverse('ValidateUser')
        self.assertEquals(resolve(url).func, ValidateUser)

    def test_AddVisit_url_is_resolved(self):
        url = reverse('AddVisit')
        self.assertEquals(resolve(url).func, AddVisit)

    def test_DeleteTask_url_is_resolved(self):
        url = reverse('DeleteTask')
        self.assertEquals(resolve(url).func, DeleteTask)

            