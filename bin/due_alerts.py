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
    due_date=str(datetime.strftime(datetime.now()+timedelta(days=1),'%Y-%m-%d'))
    anc_due_records = AncDue.objects.filter(visitdate=str(due_date),visittype="anc_visit").values_list("patientnum","womenname","anmnum","anmid")
    for anc in anc_due_records:
        patient_sms = "Dear %s, Your ANC Visit/TT/IFA/Hb Test due date is on %s" %(str(anc[1]),due_date)
        anm_sms = "Dear %s,%s ANC Visit/TT/IFA/Hb Test due date is on %s" %(str(anc[3]),str(anc[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(anc[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(anc[0]),worker_sms=anm_sms,patientsms=patient_sms)
    opv_bcg_due_date=str(datetime.strftime(datetime.now(),'%Y-%m-%d'))
    opv1_pentavalent1_due_date=str(datetime.strftime(datetime.now()-timedelta(days=settings.OPV1_PENTAVALENT1_DAYS),'%Y-%m-%d'))
    opv2_pentavalent2_due_date=str(datetime.strftime(datetime.now()-timedelta(days=settings.OPV2_PENTAVALENT2_DAYS),'%Y-%m-%d'))
    opv3_pentavalent3_due_date=str(datetime.strftime(datetime.now()-timedelta(days=settings.OPV3_PENTAVALENT3_DAYS),'%Y-%m-%d'))
    measles_due_date=str(datetime.strftime(datetime.now()+timedelta(days=settings.MEASLES_DAYS),'%Y-%m-%d'))
    mmr_due_date=str(datetime.strftime(datetime.now()+timedelta(days=settings.MMR_DAYS),'%Y-%m-%d'))
    measles2_dptbooster1_due_date=str(datetime.strftime(datetime.now()+timedelta(days=settings.MEASLES2_DPTBOOSTER1_DAYS),'%Y-%m-%d'))
    opvbooster_due_date=str(datetime.strftime(datetime.now()+timedelta(days=settings.OPVBOOSTER_DAYS),'%Y-%m-%d'))
    dptbooster2_due_date=str(datetime.strftime(datetime.now()+timedelta(days=settings.DPTBOOSTER2_DAYS),'%Y-%m-%d'))
    opv_bcg_dues = AncDue.objects.filter(lmpdate=str(opv_bcg_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")
    opv1_pentavalent1_dues = AncDue.objects.filter(lmpdate=str(opv1_pentavalent1_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")
    opv2_pentavalent2_dues = AncDue.objects.filter(lmpdate=str(opv2_pentavalent2_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")
    opv3_pentavalent3_dues = AncDue.objects.filter(lmpdate=str(opv3_pentavalent3_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")
    measles_dues = AncDue.objects.filter(lmpdate=str(measles_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")
    mmr_dues = AncDue.objects.filter(lmpdate=str(mmr_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")
    measles2_dptbooster1_dues = AncDue.objects.filter(lmpdate=str(measles2_dptbooster1_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")
    opvbooster_dues = AncDue.objects.filter(lmpdate=str(opvbooster_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")
    dptbooster2_dues = AncDue.objects.filter(lmpdate=str(dptbooster2_due_date),visittype="child_Immunization").values_list("patientnum","womenname","anmnum","anmid")

    for opv in opv_bcg_dues:
        opv_bcg_mother_sms = "Dear %s,Your Child Immunization OPV,BCG,HBV0 due date is on %s" %(str(opv[1]),due_date)
        opv_bcg_anm_sms = "Dear %s,%s Child Immunization OPV,BCG,HBV0 due date is on %s" %(str(opv[3]),str(opv[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(opv[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(opv[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

    for opv1 in opv1_pentavalent1_dues:
        opv1_pentavalent1_mother_sms = "Dear %s,Your Child Immunization OPV1,PENTAVALENT1 due date is on %s" %(str(opv1[1]),due_date)
        opv1_pentavalent1_anm_sms = "Dear %s,%s Child Immunization OPV1,PENTAVALENT1 due date is on %s" %(str(opv1[3]),str(opv1[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(opv1[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(opv1[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

    for opv2 in opv2_pentavalent2_dues:
        opv2_pentavalent2_mother_sms = "Dear %s,Your Child Immunization OPV2,PENTAVALENT2 due date is on %s" %(str(opv2[1]),due_date)
        opv2_pentavalent2_anm_sms = "Dear %s,%s Child Immunization OPV2,PENTAVALENT2 due date is on %s" %(str(opv2[3]),str(opv2[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(opv2[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(opv2[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

    for opv3 in opv3_pentavalent3_dues:
        opv3_pentavalent3_mother_sms = "Dear %s,Your Child Immunization OPV3,PENTAVALENT3 due date is on %s" %(str(opv3[1]),due_date)
        opv3_pentavalent3_anm_sms = "Dear %s,%s Child Immunization OPV3,PENTAVALENT3 due date is on %s" %(str(opv3[3]),str(opv3[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(opv3[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(opv3[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

    for measles in measles_dues:
        measles_mother_sms = "Dear %s,Your Child Immunization measles due date is on %s" %(str(measles[1]),due_date)
        measles_anm_sms = "Dear %s,%s Child Immunization measles due date is on %s" %(str(measles[3]),str(measles[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(measles[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(measles[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

    for mmr in mmr_dues:
        mmr_mother_sms = "Dear %s,Your Child Immunization MMR due date is on %s" %(str(mmr[1]),due_date)
        mmmr_anm_sms = "Dear %s,%s Child Immunization MMR due date is on %s" %(str(mmr[3]),str(mmr[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(mmr[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(mmr[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

    for measles2 in measles2_dptbooster1_dues:
        measles2_mother_sms = "Dear %s,Your Child Immunization MEASLES2 due date is on %s" %(str(measles2[1]),due_date)
        measles2_anm_sms = "Dear %s,%s Child Immunization MEASLES2 due date is on %s" %(str(measles2[3]),str(measles2[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(measles2[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(measles2[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

    for opvbooster in opvbooster_dues:
        opvbooster_mother_sms = "Dear %s,Your Child Immunization OPVBOOSTER due date is on %s" %(str(opvbooster[1]),due_date)
        opvbooster_anm_sms = "Dear %s,%s Child Immunization OPVBOOSTER due date is on %s" %(str(opvbooster[3]),str(opvbooster[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(opvbooster[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(opvbooster[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

    for dptbooster2 in dptbooster2_dues:
        dptbooster2_mother_sms = "Dear %s,Your Child Immunization DPTBOOSTER2 due date is on %s" %(str(dptbooster2[1]),due_date)
        dptbooster2_anm_sms = "Dear %s,%s Child Immunization DPTBOOSTER2 due date is on %s" %(str(dptbooster2[3]),str(dptbooster2[1]),due_date)
        country_name = UserMasters.objects.filter(user_id=str(anc[3])).values_list("country__country_name")[0][0]
        country_code = CountryTb.objects.filter(country_name=str(country_name)).values_list("country_code")[0][0]
        anmph = str(country_code)+str(str(dptbooster2[2])[-int(settings.PHONE_NUMBER_LENGTH):])
        anm_sms,patient_sms = docsms(workerph=anmph,patientph=str(dptbooster2[0]),worker_sms=opv_bcg_anm_sms,patientsms=opv_bcg_mother_sms)

if __name__ == "__main__":
    due_alerts_sms()