from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from luxmed.LuxMedAPI.LuxmedAPI import LuxMedSniper
from .forms import NameForm, VisitForm, DeleteTaskForm
from .ImportCSV import Import_LuxMedCity, Import_LuxMedService
from django.core.paginator import Paginator
from .models import MyTask
from django.utils.timezone import utc



def home(request):
    if 'username' in request.session:

        task_list = MyTask.objects.all()
        test2 = task_list[::-1]
        # To return a new list, use the sorted() built-in function...
        # = sorted(task_list, key=lambda x: x.count, reverse=True)


        page = request.GET.get('page', 1)
        paginator = Paginator(test2, 10)

        try:
            My_Tasks = paginator.page(page)
        except PageNotAnInteger:
            My_Tasks = paginator.page(1)
        except EmptyPage:
            My_Tasks = paginator.page(paginator.num_pages)


        return render(request, "luxmed/home.html", { 'My_Tasks': My_Tasks })
    else:
        return render(request, 'luxmed/Index.html')

def DeleteTask(request):
    if request.method == 'POST':
        form = DeleteTaskForm(request.POST)
            # check whether it's valid:
        if form.is_valid():
            objectos = MyTask.objects.get(id=form.cleaned_data['DeleteTaskID'])
            objectos.delete()

    return HttpResponseRedirect('/home/')



def Index(request):
    return render(request, 'luxmed/Index.html')



def AddVisit(request):
    #Import_LuxMedCity()
    #Import_LuxMedService()
    if request.method == 'POST':
        form = VisitForm(request.POST)
            # check whether it's valid:
        if form.is_valid():
            testos = form.save(commit=False)
            # commit=False tells Django that "Don't send this to database yet.
            # I have more things I want to do with it."
            #student.user = request.user # Set the user object here
            #testos.VisitDate = '2019-01-01 11:11'
            #testos.LastCheck = '2019-01-01 11:11'
            testos.save() 
            

            return HttpResponseRedirect('/home/')
            #return home(request) 

        else:
            return render(request, 'luxmed/error.html')

    else:
        initial = {'UserEmail': request.session['username'],'UserPassword': request.session['userpass']  }
        form = VisitForm(initial=initial)
        return render(request, "luxmed/AddVisit.html", {'form': form})

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
