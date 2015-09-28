__author__ = 'Eswar'
import os
import sys

script_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.abspath(os.path.dirname(script_dir))

sys.path.append(project_dir)
sys.path.append(os.path.dirname(project_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opensrp.settings")
import django
django.setup()

from Masters.models import *
from django.db import connection
from datetime import date, timedelta,datetime
from Masters.views import docsms

def due_alerts_sms():
    due_date=str(datetime.strftime(datetime.now()+timedelta(days=1),'%Y/%m/%d'))
    anc_due_records = AncDue.objects.filter(visitdate=str(due_date),visittype="anc_visit").values_list("patientnum","womenname","anmnum","anmid")
    for anc in anc_due_records:
        patient_sms = "Dear %s, Your ANC Visit/TT/IFA/Hb Test due date is on %s" %(str(anc[1]),due_date)
        anm_sms = "Dear %s,%s ANC Visit/TT/IFA/Hb Test due date is on %s" %(str(anc[3]),str(anc[1]),due_date)
        country_code = CountryTb.objects.filter(country_name=str(UserMasters.objects.filter(user_id=str(anc[3])).values_list("country_name"))).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(anc[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(anc[0]),worker_sms=anm_sms,patientsms=patient_sms)

if __name__ == "__main__":
    due_alerts_sms()