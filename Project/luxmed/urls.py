from django.urls import path
from luxmed import views

urlpatterns = [
    path("", views.hello_there, name="hello_there"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("ValidateUser/", views.ValidateUser, name="Validation"),
]