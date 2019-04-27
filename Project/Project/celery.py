import os
from celery import Celery

#Setup Celery Machine
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

#Define Celery project
app = Celery('Project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#Run Celery tasks
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))