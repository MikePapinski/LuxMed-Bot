from django.urls import path
from luxmed import views

urlpatterns = [
    path("", views.Index, name="Index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("error/", views.error, name="error"),
    path("home/", views.home, name="home"),
    path("AddVisit/", views.AddVisit, name="AddVisit"),
    path("contact/", views.contact, name="contact"),
    path("ValidateUser/", views.ValidateUser, name="Validation"),
]