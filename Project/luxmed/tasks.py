from celery import shared_task
from .models import MyTask

#Create shared task for Celery to process
@shared_task
def RefreshLuxMedVisits():
    #Get all tasks from SQL objects
    task_list = MyTask.objects.all()

    #Loop through each task
    for MyObject in task_list:
        MyObject.GetNewVisit() # Refresh the visit data
        MyObject.save() # Save the changes

    #Print to confirm the task executed without errors
    print('Job Done! - All visits refreshed') 