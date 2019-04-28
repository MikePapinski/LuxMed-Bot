from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from luxmed.LuxMedAPI.LuxmedAPI import LuxMedConnector
from .forms import VisitForm, DeleteTaskForm, LoginForm
from django.core.paginator import Paginator
from .models import MyTask
from django.utils.timezone import utc


# Home View 
def home(request):
    if 'username' in request.session:

        #Get List of all tasks and revert it to get the newest on the top
        task_list = MyTask.objects.all()
        task_list_reverted = task_list[::-1]

        #Move List to pagination table
        page = request.GET.get('page', 1)
        paginator = Paginator(task_list_reverted, 10)
        try:
            My_Tasks = paginator.page(page)
        except PageNotAnInteger:
            My_Tasks = paginator.page(1)
        except EmptyPage:
            My_Tasks = paginator.page(paginator.num_pages)

        #Return view to template
        return render(request, "luxmed/home.html", { 'My_Tasks': My_Tasks })
    else:
        return render(request, 'luxmed/Index.html')

# View to process Task Deletaion
def DeleteTask(request):
    #Check if POST request
    if request.method == 'POST':
        form = DeleteTaskForm(request.POST)
        #Check if form for delation is valid
        if form.is_valid():
            objectos = MyTask.objects.get(id=form.cleaned_data['DeleteTaskID'])
            objectos.delete() # Delete task
    #redirect to home view
    return HttpResponseRedirect('/home/')


#Return the Index page (Entry Page)
def Index(request):
    return render(request, 'luxmed/Index.html')



#Add Task Visit View
def AddVisit(request):
    #Check if POST request
    if request.method == 'POST':
        form = VisitForm(request.POST)
        # check whether form it's valid:
        if form.is_valid():
            AddViewForm = form.save(commit=False) # commit=False tells Django that "Don't send this to database yet.
            AddViewForm.save()  # save to form to database          
            #redirect to home
            return HttpResponseRedirect('/home/')
        else:
            #Not a post request, return error view
            return render(request, 'luxmed/error.html')

    else:
        # This is NOT a POST request - Return the form template
        initial = {'UserEmail': request.session['username'],'UserPassword': request.session['userpass']  }
        form = VisitForm(initial=initial)
        #Return form
        return render(request, "luxmed/AddVisit.html", {'form': form})


#Get the Contact view
def contact(request):
    return render(request, 'luxmed/contact.html')

#View to process user validation
def ValidateUser(request):
    # Check is POST request
    if request.method == 'POST':
            # Delete user session if exists
            try:
                del request.session['username']
            except:
                pass

            # create a form instance and populate it with data from the request:
            form = LoginForm(request.POST)
            # check whether form it's valid:
            if form.is_valid():


            
                #Create the LuxMedConnector Object
                NewUserSession = LuxMedConnector()
                NewUserSession.LUXemail = form.cleaned_data['your_name'] # Pass the user name/email to LuxMedConnector
                NewUserSession.LUXpassword = form.cleaned_data['your_pass'] #Pass the user password to LuxMedConnector
                NewUserSession._createSession() #Create session
                NewUserSession._logIn() #Login to LuxMed using user credentials

                #Check if user logged in to LuxMed succesfully
                if NewUserSession.LoginStatus==True:
                    request.session['username'] = NewUserSession.LUXemail # Create session for user with Email data
                    request.session['userpass'] = NewUserSession.LUXpassword # Create session for user with Pass data
 
                    return render(request, "luxmed/home.html", {"username" : NewUserSession.LUXemail}) # Success - User logged in to LuxMed
                else:
                    return render(request, "luxmed/error.html") # Error - User do not exist in LuxMed Portal
            else:

                return render(request, "luxmed/error.html") # Error - The form is not valid
    else:
        # Not a POST request, redirect to login page    
        form = LoginForm()
        return render(request, 'luxmed/login.html', {'form': form})


#Get the login page
def login(request):
    form = LoginForm()
    return render(request, 'luxmed/login.html', {'form': form})

#View to process logout request
def logout(request):
    try:
        del request.session['username'] # Delete session if exists
    except:
        pass
    return render(request, 'luxmed/Index.html') # Redirect to Main Index Page

#Return the error view
def error(request):
    return render(request, 'luxmed/error.html')
