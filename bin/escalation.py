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
from Masters.views import patientsms, anmsms

def level_escalation(country):
    country = CountryTb.objects.filter(country_name=str(country)).values_list("id")
    if len(country)>0:
        country_id=country[0][0]
    minutes = str(AppConfiguration.objects.filter(country_name=country_id).values_list("escalation_schedule")[0][0])
    cur = connection.cursor()
    query = "SELECT level,phc,pending,visitentityid,entityidec,wifename FROM report.poc_table WHERE timestamp <= (now() - '%s   minutes'::INTERVAL);" %minutes
    cur.execute(str(query))
    poc_details = cur.fetchall()
    print poc_details,"poc details"
    if len(poc_details)>0:
        print "if"
        for poc in poc_details:
            print poc,"single poc"
            print poc[-1],poc[2]
            if str(poc[0]) == "1" and len(str(poc[2]))>=0:
                level = int(poc[0])+1
                print poc[1],"hospital_name"
                location_details = HealthCenters.objects.filter(hospital_name=str(poc[1]),hospital_type='PHC').values_list("parent_hospital","id")
                location = location_details[0][0]
                location_id= location_details[0][1]
                print location,"location"
                doctor_details = UserMasters.objects.filter(hospital=location_id).values_list("name","phone_number","country")
                for doctor in doctor_details:
                    print doctor[-1],"doc"
                    print CountryTb.objects.filter(country_name=str(doctor[-1]))
                    country_code=str(CountryTb.objects.filter(id=doctor[-1]).values_list("country_code")[0][0])
                    doctor_phone=country_code+str(doctor[2])[-int(settings.PHONE_NUMBER_LENGTH):]
                    doc_sms= anmsms(workerph=doctor_phone,worker_sms="Patient escalated to SubDistrict level")
                update_level = PocInfo.objects.filter(visitentityid=str(poc[3]),entityidec=str(poc[4])).update(level=str(level),phc=str(location),timestamp=datetime.now())
            elif str(poc[0]) == "2" and str(poc[2])=='None':
                level = int(poc[0])+1
                location_details = HealthCenters.objects.filter(hospital_name=str(poc[1]),hospital_type='PHC').values_list("parent_hospital","id")
                location = location_details[0][0]
                location_id= location_details[0][1]
                print location,"location"
                doctor_details = UserMasters.objects.filter(hospital=location_id).values_list("name","phone_number","country")
                for doctor in doctor_details:
                    country_code=str(CountryTb.objects.filter(id=doctor[-1]).values_list("country_code")[0][0])
                    doctor_phone=country_code+str(doctor[2])[-int(settings.PHONE_NUMBER_LENGTH):]
                    doc_sms= anmsms(workerph=doctor_phone,worker_sms="Patient escalated to District level")
                update_level = PocInfo.objects.filter(visitentityid=str(poc[3]),entityidec=str(poc[4])).update(level=str(level),phc=str(location),timestamp=datetime.now())
            elif str(poc[0]) == "3" and str(poc[2])=='None':
                level = int(poc[0])+1
                location_details = HealthCenters.objects.filter(hospital_name=str(poc[1]),hospital_type='PHC').values_list("parent_hospital","id")
                location = location_details[0][0]
                location_id= location_details[0][1]
                print location,"location"
                doctor_details = UserMasters.objects.filter(hospital=location_id).values_list("name","phone_number","country")
                for doctor in doctor_details:
                    country_code=str(CountryTb.objects.filter(id=doctor[-1]).values_list("country_code")[0][0])
                    doctor_phone=country_code+str(doctor[2])[-int(settings.PHONE_NUMBER_LENGTH):]
                    doc_sms = anmsms(workerph=doctor_phone,worker_sms="Patient escalated to County level")
                update_level = PocInfo.objects.filter(visitentityid=str(poc[3]),entityidec=str(poc[4])).update(level=str(level),phc=str(location),timestamp=datetime.now())
            elif str(poc[0]) == "4" and str(poc[2])=='None':
                level = int(poc[0])+1
                location_details = HealthCenters.objects.filter(hospital_name=str(poc[1]),hospital_type='PHC').values_list("parent_hospital","id")
                location = location_details[0][0]
                location_id= location_details[0][1]
                print location,"location"
                doctor_details = UserMasters.objects.filter(hospital=location_id).values_list("name","phone_number","country")
                for doctor in doctor_details:
                    country_code=str(CountryTb.objects.filter(id=doctor[-1]).values_list("country_code")[0][0])
                    doctor_phone=country_code+str(doctor[2])[-int(settings.PHONE_NUMBER_LENGTH):]
                    doc_sms = anmsms(workerph=doctor_phone,worker_sms="Patient escalated to Country level")
                update_level = PocInfo.objects.filter(visitentityid=str(poc[3]),entityidec=str(poc[4])).update(level=str(level),phc=str(location),timestamp=datetime.now())

if __name__ == "__main__":
    print sys.argv
    country = sys.argv[1]
    level_escalation(country)