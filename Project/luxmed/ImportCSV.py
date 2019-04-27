import csv
import sys
from .models import LuxMedLocation,LuxMedService

# Import LuxMedCity to SQL Database
def Import_LuxMedCity():

    with open('/code/Project/luxmed/LuxMedAPI/LuxMedCity.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            MyCityObject = LuxMedLocation.objects.get_or_create(LuxMedID = row[0],LocationName = row[1])

# Import LuxMed Service to SQL Database
def Import_LuxMedService():

    with open('/code/Project/luxmed/LuxMedAPI/LuxMedService.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            MyServiceObject = LuxMedService.objects.get_or_create(LuxMedID = row[0],ServiceName = row[1])


# Call those procedures on startup
Import_LuxMedCity()
Import_LuxMedService()