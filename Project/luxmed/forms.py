from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='',max_length=100) 
    your_pass = forms.CharField(label='',max_length=100, widget=forms.PasswordInput())

    your_name.widget.attrs['class'] = 'form-control'
    your_pass.widget.attrs['class'] = 'form-control'

    your_name.widget.attrs['placeholder'] = 'Your LuxMed Email *'
    your_pass.widget.attrs['placeholder'] = 'Your LuxMed Password *'

    your_name.widget.attrs['type'] = 'text'
    your_pass.widget.attrs['type'] = 'password'