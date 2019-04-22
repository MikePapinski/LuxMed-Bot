import requests
from bs4 import BeautifulSoup
import argparse
import yaml
import logging
import os
import datetime
import shelve
import time
from datetime import date





class LuxMedSniper():
    LUXMED_LOGIN_URL = 'https://portalpacjenta.luxmed.pl/PatientPortal/Account/LogIn'
    LUXMED_LOGOUT_URL = 'https://portalpacjenta.luxmed.pl/PatientPortal/Account/LogOn'
    MAIN_PAGE_URL = 'https://portalpacjenta.luxmed.pl/PatientPortal'
    REQUEST_RESERVATION_URL = 'https://portalpacjenta.luxmed.pl/PatientPortal/Reservations/Reservation/PartialSearch'
    LUXemail= ""
    LUXpassword= ""
    LoginStatus = False

    Find_Location = ""
    Find_Service = ""

   # def __init__(self):



    def _createSession(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
        self.session.headers.update(
            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'})
        self.session.headers.update({'Referer': self.LUXMED_LOGOUT_URL})
        self.session.cookies.update({'LXCookieMonit': '1'})


    def _logIn(self):
        login_data = {'LogIn': self.LUXemail, 'Password': self.LUXpassword}
        resp = self.session.post(self.LUXMED_LOGIN_URL, login_data)
        if resp.text.find('Nieprawidłowy login lub hasło.') != -1:
            self.LoginStatus = False
        else:
            soup = BeautifulSoup(resp.text, "html.parser")
            self.requestVerificationToken = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
            self.LoginStatus = True

    def _parseVisits(self, page_data):
        s = BeautifulSoup(page_data, "html.parser")
        appointments = []
        visits = s.findAll('li')
        for visit in visits:
            date = visit.find('div', {'class': 'col-md-8'})
            if not date:
                continue
            date = date.getText().strip()
            reserveTable = visit.find('table', {'class': 'reserveTable'})
            for reservation in reserveTable.findAll('tr')[1:]:
                if reservation.find('td', {'class': 'action-buttons'}):
                    continue
                divs = reservation.findAll('div')
                time = divs[0].getText().strip()[:-9]
                doctorName = divs[1].getText().strip()
                serviceName = divs[2].getText().strip()
                location = divs[3].getText().strip()
                rest = divs[4:]
                additionalInfo = []
                for res in rest:
                    additionalInfo.append(" ".join(res.getText().split()))
                appointments.append(
                    {'AppointmentDate': '%s %s' % (date, time), 'ClinicPublicName': location, 'DoctorName': doctorName,
                     'SpecialtyName': serviceName, 'AdditionalInfo': " ".join(additionalInfo)})
        return appointments

    def _getAppointments(self):
        
            data = {
                '__RequestVerificationToken': self.requestVerificationToken,
                'DateOption': 'SelectedDate',
                'FilterType': 'Coordination',
                'CoordinationActivityId': 16,
                'IsFFS': 'False',
                'MaxPeriodLength': 0,
                'IsDisabled': 'False',
                'PayersCount': 0,
                'FromDate': date.today(),
                'ToDate': date.today() + datetime.timedelta(days=90),
                'DefaultSearchPeriod': 90,
                'CustomRangeSelected': 'False',
                'SelectedSearchPeriod': 90,
                'CityId': self.Find_Location,
                'DateRangePickerButtonDefaultLabel': 'Inny zakres',
                'ServiceId': self.Find_Service,
                'TimeOption': 3,
                'PayerId': 0,
                'LanguageId': ''
                }

            data['ClinicId'] = -1

            data['DoctorMultiIdentyfier'] = -1

            r = self.session.post(self.REQUEST_RESERVATION_URL, data)

            
            return self._parseVisits(r.text)



