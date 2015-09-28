__author__ = 'Eswar'

'''
Case level escalation cron job
'''
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

def level_escalation():
    minutes = str(AppConfiguration.objects.all().values_list("escalation_schedule")[0][0])
    cur = connection.cursor()
    query = "SELECT level,phc,pending,visitentityid,entityidec FROM report.poc_table WHERE timestamp <= (now() - '%s   minutes'::INTERVAL);" %minutes
    cur.execute(str(query))
    poc_details = cur.fetchall()
    if len(poc_details)>0 :
        for poc in poc_details:
            if str(poc[0]) == "1" and str(poc[2])=='None':
                level = int(poc[0])+1
                location = HealthCenters.objects.filter(hospital_name=str(poc[1]),hospital_type='PHC').values_list("parent_hospital")[0][0]
                doctor_details = UserMasters.objects.filter(hospital_name=str(location)).values_list("name","phone_number","country")
                for doctor in doctor_details:
                    country_code=str(CountryTb.objects.filter(country_name=str(doctor[3])).values_list("country_code")[0][0])
                    doctor_phone=country_code+str(doctor[2])[-int(settings.PHONE_NUMBER_LENGTH):]
                    doc_sms,junk_sms = docsms(workerph=doctor_phone,worker_sms="Patient escalated to SubDistrict level")
                update_level = PocInfo.objects.filter(visitentityid=str(poc[3]),entityidec=str(poc[4])).update(level=str(level),phc=str(location),timestamp=datetime.now())
            elif str(poc[0]) == "2" and str(poc[2])=='None':
                level = int(poc[0])+1
                location = HealthCenters.objects.filter(hospital_name=str(poc[1]),hospital_type='SubDistrict').values_list("parent_hospital")[0][0]
                doctor_details = UserMasters.objects.filter(hospital_name=str(location)).values_list("name","phone_number","country")
                for doctor in doctor_details:
                    country_code=str(CountryTb.objects.filter(country_name=str(doctor[3])).values_list("country_code")[0][0])
                    doctor_phone=country_code+str(doctor[2])[-int(settings.PHONE_NUMBER_LENGTH):]
                    doc_sms,junk_sms = docsms(workerph=doctor_phone,worker_sms="Patient escalated to District level")
                update_level = PocInfo.objects.filter(visitentityid=str(poc[3]),entityidec=str(poc[4])).update(level=str(level),phc=str(location),timestamp=datetime.now())
            elif str(poc[0]) == "3" and str(poc[2])=='None':
                level = int(poc[0])+1
                location = HealthCenters.objects.filter(hospital_name=str(poc[1]),hospital_type='District').values_list("parent_hospital")[0][0]
                doctor_details = UserMasters.objects.filter(hospital_name=str(location)).values_list("name","phone_number","country")
                for doctor in doctor_details:
                    country_code=str(CountryTb.objects.filter(country_name=str(doctor[3])).values_list("country_code")[0][0])
                    doctor_phone=country_code+str(doctor[2])[-int(settings.PHONE_NUMBER_LENGTH):]
                    doc_sms,junk_sms = docsms(workerph=doctor_phone,worker_sms="Patient escalated to County level")
                update_level = PocInfo.objects.filter(visitentityid=str(poc[3]),entityidec=str(poc[4])).update(level=str(level),phc=str(location),timestamp=datetime.now())
            elif str(poc[0]) == "4" and str(poc[2])=='None':
                level = int(poc[0])+1
                location = HealthCenters.objects.filter(hospital_name=str(poc[1]),hospital_type='County').values_list("parent_hospital")[0][0]
                doctor_details = UserMasters.objects.filter(hospital_name=str(location)).values_list("name","phone_number","country")
                for doctor in doctor_details:
                    country_code=str(CountryTb.objects.filter(country_name=str(doctor[3])).values_list("country_code")[0][0])
                    doctor_phone=country_code+str(doctor[2])[-int(settings.PHONE_NUMBER_LENGTH):]
                    doc_sms,junk_sms = docsms(workerph=doctor_phone,worker_sms="Patient escalated to Country level")
                update_level = PocInfo.objects.filter(visitentityid=str(poc[3]),entityidec=str(poc[4])).update(level=str(level),phc=str(location),timestamp=datetime.now())

if __name__ == "__main__":
    level_escalation()