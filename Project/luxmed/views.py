from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from luxmed.LuxMedAPI.LuxmedAPI import LuxMedSniper
from .forms import NameForm




def home(request):
    if 'username' in request.session:
        return render(request, "luxmed/home.html")
    else:
        return render(request, 'luxmed/Index.html')

def Index(request):
    return render(request, 'luxmed/Index.html')



def AddVisit(request):
        return render(request, "luxmed/AddVisit.html")

def contact(request):
        return render(request, 'luxmed/contact.html')

def ValidateUser(request):
    if request.method == 'POST':
            try:
                del request.session['username']
            except:
                pass

            # create a form instance and populate it with data from the request:
            form = NameForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                test = LuxMedSniper()
                test.LUXemail = form.cleaned_data['your_name']
                test.LUXpassword = form.cleaned_data['your_pass']
                test._createSession()
                test._logIn()

                if test.LoginStatus==True:
                    request.session['username'] = test.LUXemail
                    request.session['userpass'] = test.LUXpassword
                    return render(request, "luxmed/home.html", {"username" : test.LUXemail})
                else:
                    return render(request, "luxmed/error.html")
            else:
                return render(request, "luxmed/error.html")
    else:    
        form = NameForm()
        return render(request, 'luxmed/login.html', {'form': form})



def login(request):
    form = NameForm()
    return render(request, 'luxmed/login.html', {'form': form})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'luxmed/Index.html')

def error(request):
    del request.session['username']
    return render(request, 'luxmed/error.html')
