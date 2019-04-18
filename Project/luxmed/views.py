from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
# Create your views here.


from .forms import NameForm
def hello_there(request):
   # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, 'luxmed/hello_there.html', {'form': form})



def home(request):
        return render(request, "luxmed/home.html")

def about(request):
    return render(request, "luxmed/about.html")

def contact(request):
    return render(request, "luxmed/contact.html")


def ValidateUser(request):
    if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = NameForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
               

                if form.cleaned_data['your_name'] == 'Majki' and form.cleaned_data['your_pass'] == 'Majki':
                    return HttpResponse("Welcome Majki")
                else:
                    return HttpResponse('not authorized')
            else:
                return render(request, "luxmed/contact.html")
    else:    
        form = NameForm()
        return render(request, 'luxmed/hello_there.html', {'form': form})