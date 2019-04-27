from django import forms
from luxmed.models import MyTask
from django.contrib.admin import widgets
import datetime


#Form to Login
class LoginForm(forms.Form):
    your_name = forms.CharField(label='',max_length=100) 
    your_pass = forms.CharField(label='',max_length=100, widget=forms.PasswordInput())

    your_name.widget.attrs['class'] = 'form-control'
    your_pass.widget.attrs['class'] = 'form-control'

    your_name.widget.attrs['placeholder'] = 'Your LuxMed Email *'
    your_pass.widget.attrs['placeholder'] = 'Your LuxMed Password *'

    your_name.widget.attrs['type'] = 'text'
    your_pass.widget.attrs['type'] = 'password'


#Form to delete task
class DeleteTaskForm(forms.Form):
    DeleteTaskID = forms.CharField(label='',max_length=100) 



#Form to add 
class VisitForm(forms.ModelForm):
    class Meta:
        model = MyTask     # Create form from this model
        fields = ['UserEmail', 'UserPassword', 'City', 'Service','TimeFrom','TimeTo','WhatsappNr']

        TIME_CHOICES= [
        ('07:00', '07:00'),
        ('07:15', '07:15'),
        ('07:30', '07:30'),
        ('07:45', '07:45'),
        ('08:00', '08:00'),
        ('08:15', '08:15'),
        ('08:30', '08:30'),
        ('08:45', '08:45'),
        ('09:00', '09:00'),
        ('09:15', '09:15'),
        ('09:30', '09:30'),
        ('09:45', '09:45'),
        ('10:00', '10:00'),
        ('10:15', '10:15'),
        ('10:30', '10:30'),
        ('10:45', '10:45'),
        ('11:00', '11:00'),
        ('11:15', '11:15'),
        ('11:30', '11:30'),
        ('11:45', '11:45'),
        ('12:00', '12:00'),
        ('12:15', '12:15'),
        ('12:30', '12:30'),
        ('12:45', '12:45'),
        ('13:00', '13:00'),
        ('13:15', '13:15'),
        ('13:30', '13:30'),
        ('13:45', '13:45'),
        ('14:00', '14:00'),
        ('14:15', '14:15'),
        ('14:30', '14:30'),
        ('14:45', '14:45'),
        ('15:00', '15:00'),
        ('15:15', '15:15'),
        ('15:30', '15:30'),
        ('15:45', '15:45'),
        ('16:00', '16:00'),
        ('16:15', '16:15'),
        ('16:30', '16:30'),
        ('16:45', '16:45'),
        ('17:00', '17:00'),
        ('17:15', '17:15'),
        ('17:30', '17:30'),
        ('17:45', '17:45'),
        ('18:00', '18:00'),
        ('18:15', '18:15'),
        ('18:30', '18:30'),
        ('18:45', '18:45'),
        ('19:00', '19:00'),
        ('19:15', '19:15'),
        ('19:30', '19:30'),
        ('19:45', '19:45'),
        ('20:00', '20:00'),
        ('20:15', '20:15'),
        ('20:30', '20:30'),
        ('20:45', '20:45'),
        ('21:00', '21:00'),
        ('21:15', '21:15'),
        ('21:30', '21:30'),
        ('21:45', '21:45'),
        ]

        #Add widgets
        widgets = {
            'UserPassword': forms.PasswordInput(),
            'TimeFrom': forms.Select(choices=TIME_CHOICES),
            'TimeTo': forms.Select(choices=TIME_CHOICES)
            }

    def __init__(self, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)
        d = datetime.datetime.now().year
        ch = [(X,X) for X in range(2005, d)]
        self.fields['TimeFrom'].choices = ch
        self.fields['TimeTo'].choices = ch
        


