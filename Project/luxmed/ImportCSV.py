import csv
import sys
#sys.path.append("..") # Adds higher directory to python modules path.
from .models import LuxMedLocation,LuxMedService

def Import_LuxMedCity():

    with open('/code/Project/luxmed/LuxMedAPI/LuxMedCity.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
           # print(row[0] + row[1])
            MyCityObject = LuxMedLocation.objects.get_or_create(LuxMedID = row[0],LocationName = row[1])


def Import_LuxMedService():

    with open('/code/Project/luxmed/LuxMedAPI/LuxMedService.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
          #  print(row[0] + row[1])
            MyServiceObject = LuxMedService.objects.get_or_create(LuxMedID = row[0],ServiceName = row[1])


Import_LuxMedCity()
Import_LuxMedService()