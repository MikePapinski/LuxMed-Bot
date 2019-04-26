from celery import shared_task
from .models import MyTask

@shared_task
def RefreshLuxMedVisits():
    task_list = MyTask.objects.all()

    for MyObject in task_list:
        MyObject.GetNewVisit()
        MyObject.save()

    

    print('Job Done! - All visits refreshed') 