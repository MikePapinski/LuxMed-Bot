import requests
from bs4 import BeautifulSoup
import argparse
import yaml
import logging
import os
import datetime
import shelve
import time



class LuxMedAPI:
    LUXMED_LOGIN_URL = 'https://portalpacjenta.luxmed.pl/PatientPortal/Account/LogIn'
    LUXMED_LOGOUT_URL = 'https://portalpacjenta.luxmed.pl/PatientPortal/Account/LogOn'
    MAIN_PAGE_URL = 'https://portalpacjenta.luxmed.pl/PatientPortal'
    REQUEST_RESERVATION_URL = 'https://portalpacjenta.luxmed.pl/PatientPortal/Reservations/Reservation/PartialSearch'

    def __init__(self, configuration_file="luxmedSniper.yaml"):
        self.log = logging.getLogger("LuxMedSniper")
        self.log.info("LuxMedSniper logger initialized")
        # Open configuration file

        self._loadConfiguration(configuration_file)
        self._createSession()
        self._logIn()

    def _createSession(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
        self.session.headers.update(
            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'})
        self.session.headers.update({'Referer': self.LUXMED_LOGOUT_URL})
        self.session.cookies.update({'LXCookieMonit': '1'})

    def _loadConfiguration(self, configuration_file):
        try:
            config_data = open(
                os.path.expanduser(
                    configuration_file
                ),
                'r'
            ).read()
        except IOError:
            raise Exception('Cannot open configuration file ({file})!'.format(file=configuration_file))
        try:
            self.config = yaml.load(config_data, Loader=yaml.FullLoader)
        except Exception as yaml_error:
            raise Exception('Configuration problem: {error}'.format(error=yaml_error))

    def _logIn(self):
        login_data = {'LogIn': self.config['luxmed']['email'], 'Password': self.config['luxmed']['password']}
        resp = self.session.post(self.LUXMED_LOGIN_URL, login_data)
        if resp.text.find('Nieprawidłowy login lub hasło.') != -1:
            raise Exception("Login or password is incorrect")
        soup = BeautifulSoup(resp.text, "html.parser")
        self.requestVerificationToken = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
        self.log.info("Successfully logged in! (RequestVerificationToken: {token}".format(
            token=self.requestVerificationToken
        ))

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
        try:
            (city_id, service_id, clinic_id, doctor_multi_identyfier) = self.config['luxmedsniper'][
                'doctor_locator_id'].strip().split('*')
        except ValueError:
            raise Exception('DoctorLocatorID seems to be in invalid format')
        data = {
            '__RequestVerificationToken': self.requestVerificationToken,
            'DateOption': 'SelectedDate',
            'FilterType': 'Ffs',
            'CoordinationActivityId': 0,
            'IsFFS': 'True',
            'MaxPeriodLength': 0,
            'IsDisabled': 'True',
            'PayersCount': 0,
            'FromDate': datetime.datetime.now().strftime("%d.%m.%Y"),
            'ToDate': datetime.datetime.now() + datetime.timedelta(days=self.config['luxmedsniper']['lookup_time_days']),
            'DefaultSearchPeriod': 14,
            'CustomRangeSelected': 'True',
            'SelectedSearchPeriod': 14,
            'CityId': city_id,
            'DateRangePickerButtonDefaultLabel': 'Inny zakres',
            'ServiceId': service_id,
            'TimeOption': 0,
            'PayerId': '',
            'LanguageId': ''}
        if clinic_id != -1:
            data['ClinicId'] = clinic_id
        if doctor_multi_identyfier != -1:
            data['DoctorMultiIdentyfier'] = doctor_multi_identyfier

        r = self.session.post(self.REQUEST_RESERVATION_URL, data)
        return self._parseVisits(r.text)

    def check(self):
        appointments = self._getAppointments()
        if not appointments:
            self.log.info("No appointments found.")
            return
        for appointment in appointments:
            self.log.info(
                "Appointment found! {AppointmentDate} at {ClinicPublicName} - {DoctorName} ({SpecialtyName}) {AdditionalInfo}".format(
                    **appointment))
            if not self._isAlreadyKnown(appointment):
                self._addToDatabase(appointment)
                self._sendNotification(appointment)
            else:
                self.log.info('Notification was already sent.')

    def _addToDatabase(self, appointment):
        db = shelve.open(self.config['misc']['notifydb'])
        notifications = db.get(appointment['DoctorName'], [])
        notifications.append(appointment['AppointmentDate'])
        db[appointment['DoctorName']] = notifications
        db.close()

    def _sendNotification(self, appointment):
        self.pushoverClient.send_message(self.config['pushover']['message_template'].format(
            **appointment, title=self.config['pushover']['title']))

    def _isAlreadyKnown(self, appointment):
        db = shelve.open(self.config['misc']['notifydb'])
        notifications = db.get(appointment['DoctorName'], [])
        db.close()
        if appointment['AppointmentDate'] in notifications:
            return True
        return False

def work(config):
    try:
        luxmedSniper = LuxMedSniper(configuration_file=config)
        luxmedSniper.check()
    except Exception as s:
        log.error(s)

if __name__ == "__main__":
    log.info("LuxMedSniper - Lux Med Appointment Sniper")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config",
        help="Configuration file path", default="luxmedSniper.yaml"
    )
    args = parser.parse_args()
    work(args.config)
    schedule.every(30).seconds.do(work, args.config)
    while True:
        schedule.run_pending()
        time.sleep(1)
