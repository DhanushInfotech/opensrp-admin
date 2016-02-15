from __future__ import unicode_literals
import json
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
import hashlib
import commands
from django.shortcuts import render_to_response, redirect, get_object_or_404
from multiselectfield import MultiSelectField

class DrugInfo(models.Model):
    ANC = (('Pallor', 'Pallor'),
               ('Swelling', 'Swelling / Edema'),
               ('Bleeding', 'Bleeding'),
               ('Jaundice', 'Jaundice'),
               ('Convulsions', 'Fits / Convulsions'))
    PNC = (('Difficult Breathing', 'Difficult Breathing'),
               ('Bad Headache', 'Bad Headache'),
               ('Blurred Vision', 'Blurred Vision'),
               ('Uterus is soft or tender', 'Uterus is soft or tender'),
               ('Abdominal Pain', 'Abdominal Pain'),
               ('Bad Smelling lochea', 'Bad Smelling lochea'),
               ('Heavy Bleeding per vaginum', 'Heavy Bleeding per vaginum'),
               ('Infected perineum suture', 'Infected perineum suture'),
               ('Difficulty Passing Urine', 'Difficulty Passing Urine'),
               ('Burning sensation when urinating', 'Burning sensation when urinating'),
               ('Breast Hardness', 'Breast Hardness'),
               ('Nipple Hardness', 'Nipple Hardness'))
    CHILD = (('Mealses', 'Mealses'),
               ('Diarrhea and dehydration', 'Diarrhea and dehydration'),
               ('Malaria', 'Malaria'),
               ('Acute Respiratory Infection', 'Acute Respiratory Infection'),
               ('Severe Acute Mal Nutrition', 'Severe Acute Mal Nutrition'),
               ('Cough', 'Cough'),
               ('Diarrhea', 'Diarrhea'),
               ('Fever', 'Fever'),
               ('Convulsions', 'Convulsions'),
               ('Vomiting', 'Vomiting'))
    #id = models.IntegerField(primary_key=True)  # AutoField?
    drug_name = models.CharField(unique=True, max_length=100)
    frequency = models.ForeignKey('Frequency', db_column='frequency',null=True,blank=True,limit_choices_to={'active': True},on_delete=models.SET_NULL)
    dosage = models.ForeignKey('Dosage', db_column='dosage',null=True,blank=True,limit_choices_to={'active': True},on_delete=models.SET_NULL)
    direction = models.ForeignKey('Directions', db_column='direction',null=True,blank=True,limit_choices_to={'active': True},on_delete=models.SET_NULL)
    anc_conditions = MultiSelectField(choices=ANC,null=True,blank=True)
    pnc_conditions = MultiSelectField(choices=PNC,null=True,blank=True)
    child_illness = MultiSelectField(choices=CHILD,null=True,blank=True)
    active = models.BooleanField(default=True)

    class Meta:

        db_table = 'drug_info'
        verbose_name_plural="DRUG INFO"
        verbose_name='DRUG INFO'
    def __unicode__(self):
        return self.drug_name


    
class Frequency(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    number_of_times = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:

        db_table = 'frequency'
        verbose_name_plural="FREQUENCIES"
	verbose_name='FREQUENCY'

    def __unicode__(self):
        return unicode(self.number_of_times)

class Dosage(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    dosage = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:

        db_table = 'dosage'
        verbose_name_plural="DOSAGE"
	verbose_name='DOSAGE'
    def __unicode__(self):
        return self.dosage

class Directions(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    directions = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    class Meta:

        db_table = 'directions'
        verbose_name_plural = "DIRECTION"
	verbose_name='DIRECTION'
    def __unicode__(self):
        return self.directions

class Investigations(models.Model):
    INVESTIGATION_SERVICE_GROUP= (('radiology','Radiology'),
		                          ('laboratory','Laboratory'),
		                          ('procedures','Procedures'),
    )
    #id = models.IntegerField(primary_key=True)  # AutoField?
    service_group_name = models.CharField(max_length=200,choices=INVESTIGATION_SERVICE_GROUP)
    investigation_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:

        db_table = 'investigation'
        verbose_name_plural = "INVESTIGATIONS"
	verbose_name='INVESTIGATION'

    def __unicode__(self):
        return self.investigation_name

class ICD10(models.Model):
    ICD10CHAPTER = (('I - Certain infectious and parasitic diseases (A00-B99)','I- Certain infectious and parasitic diseases (A00-B99)'),
               ('II - Neoplasms (C00-D48)','II   - Neoplasms (C00-D48)'),
               ('III - Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism (D50-D89)','III - Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism (D50-D89)'),
               ('IV - Endocrine, nutritional and metabolic diseases (E00-E90)','IV - Endocrine, nutritional and metabolic diseases (E00-E90)'),
               ('V - Mental and behavioral disorders (F00-F99)','V - Mental and behavioral disorders (F00-F99)'),
               ('VI - Diseases of the nervous system (G00-G99)','VI - Diseases of the nervous system (G00-G99)'),
               ('VII - Diseases of the eye and adnexa (H00-H59)','VII - Diseases of the eye and adnexa (H00-H59)'),
               ('VIII - Diseases of the ear and mastoid process (H60-H95)','VIII - Diseases of the ear and mastoid process (H60-H95)'),
               ('IX - Diseases of the circulatory system (I00-I99)','IX - Diseases of the circulatory system (I00-I99)'),
               ('X - Diseases of the respiratory system (J00-J99)','X - Diseases of the respiratory system (J00-J99)'),
               ('XI - Diseases of the digestive system (K00-K93)','XI - Diseases of the digestive system (K00-K93)'),
               ('XII - Diseases of the skin and subcutaneous tissue (L00-L99)','XII - Diseases of the skin and subcutaneous tissue (L00-L99)'),
               ('XIII - Diseases of the musculoskeletal system and connective tissue (M00-M99)','XIII - Diseases of the musculoskeletal system and connective tissue (M00-M99)'),
               ('XIV - Diseases of the genitourinary system (N00-N99)','XIV - Diseases of the genitourinary system (N00-N99)'),
               ('XV - Pregnancy, childbirth and the puerperium (O00-O99)','XV - Pregnancy, childbirth and the puerperium (O00-O99)'),
               ('XVI - Certain conditions originating in the perinatal period (P00-P96)','XVI - Certain conditions originating in the perinatal period (P00-P96)'),
               ('XVII - Congenital malformations, deformations and chromosomal abnormalities (Q00-Q99)','XVII - Congenital malformations, deformations and chromosomal abnormalities (Q00-Q99)'),
               ('XVIII - Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)','XVIII - Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)'),
               ('XIX - Injury, poisoning and certain other consequences of external causes (S00-T98)','XIX - Injury, poisoning and certain other consequences of external causes (S00-T98)'),
               ('XX - External causes of morbidity and mortality (V01-Y98)','XX - External causes of morbidity and mortality (V01-Y98)'),
               ('XXI - Factors influencing health status and contact with health services (Z00-Z99)','XXI - Factors influencing health status and contact with health services (Z00-Z99)'),
               ('XXII - Codes for special purposes (U00-U99)','XXII - Codes for special purposes (U00-U99)'),
    )
    ICD10_Chapter = models.CharField(max_length=200,choices=ICD10CHAPTER) 
    ICD10_Code = models.CharField(max_length=100) 
    ICD10_Name = models.CharField(max_length=100) 
    can_select = models.BooleanField(default=True) 
    status = models.BooleanField(default= True) 

    class Meta:

        db_table = 'icd10'
        verbose_name_plural="ICD10 CODES"
	verbose_name='ICD10 CODE'

    def __unicode__(self):
        return self.ICD10_Name

class PocInfo(models.Model):
    visitentityid = models.CharField(max_length=100) # AutoField?
    entityidec = models.CharField(max_length=100)
    anmid = models.CharField(max_length=100)
    level = models.CharField(max_length=35)
    clientversion = models.CharField(max_length=35)
    serverversion = models.CharField(max_length=35)
    visittype = models.CharField(max_length=35)
    phc = models.CharField(max_length=100)
    pending = models.CharField(max_length=300, blank=True)
    docid = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    wifename = models.CharField(max_length=200, blank=True)

    class Meta:

        db_table = 'poc_table'
        verbose_name_plural="POC INFO"
	verbose_name='POC INFO'
    def __unicode__(self):
        return unicode(self.visitentityid)

class PocBackup(models.Model):
    #id = models.IntegerField(primary_key=True)
    visitentityid = models.CharField(max_length=100)
    entityidec = models.CharField(max_length=100, blank=True)
    anmid = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=35, blank=True)
    clientversion = models.CharField(max_length=35, blank=True)
    serverversion = models.CharField(max_length=35, blank=True)
    visittype = models.CharField(max_length=35, blank=True)
    phc = models.CharField(max_length=100, blank=True)
    docid = models.CharField(max_length=100, blank=True)
    poc = models.CharField(max_length=1000, blank=True)
    class Meta:

        db_table = 'poc_backup'

class UserMasters(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    user_role = models.CharField(max_length=200)
    user_id = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    confirm_password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    country = models.ForeignKey('CountryTb', db_column='country',limit_choices_to={'active': True})
    county = models.ForeignKey('CountyTb', db_column='county',null=True,blank=True,limit_choices_to={'active': True})
    district = models.ForeignKey('Disttab', db_column='district',null=True,limit_choices_to={'active': True})
    subdistrict = models.ForeignKey('SubdistrictTab', db_column='subdistrict',null=True,limit_choices_to={'active': True})
    subcenter = models.ForeignKey('HealthCenters', db_column='subcenter',related_name='subcenter',limit_choices_to={'active': True},null=True, blank=True)
    villages = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    hospital = models.ForeignKey('HealthCenters', db_column='hospital',limit_choices_to={'active': True},null=True, blank=True)

    class Meta:
        #db_table = 'user_masters_test'
        verbose_name_plural="USERS"
        verbose_name="USERS"
        db_table = 'user_masters_new'


    def __unicode__(self):
        return str(self.user_id)
    

@receiver(post_save, sender=UserMasters)
def usermaintenance_post(sender,instance,**kwargs):
    user_role = settings.USER_ROLE[str(instance.user_role)]
    #print
    user_curl = "curl -s -H -X GET http://202.153.34.169:5984/drishti/_design/DrishtiUser/_view/by_username?key="+"%22"+str(instance.user_id)+"%22"
    user_data = commands.getoutput(user_curl) 
    output = json.loads(user_data)
    output = dict(output)
    row = output['rows']
    if len(row)>0:
        id_val = dict(output['rows'][0])
        rev_curl = "curl -s -H -X GET http://202.153.34.169:5984/drishti/"+id_val['id']
        rev_data = commands.getoutput(rev_curl)
        rev_data = dict(json.loads(rev_data))
        delet_curl = "curl -X DELETE http://202.153.34.169:5984/drishti/"+id_val['id']+"/?rev\="+rev_data['_rev']
        user_data = commands.getoutput(delet_curl)
    cmd = '''curl -s -H Content-Type:application/json -d '{"docs": [{"type": "DrishtiUser","username": "%s","password": "%s","active": true,"roles": ["%s"]  } ]}' -X POST http://202.153.34.169:5984/drishti/_bulk_docs''' %(str(instance.user_id),str(instance.password),str(user_role))
    res = commands.getstatusoutput(cmd)
    
post_save.connect(usermaintenance_post,sender=UserMasters)

class CountryTb(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    country_name = models.CharField(max_length=100)
    country_code=models.CharField(max_length=10)
    active = models.BooleanField(default=True)

    class Meta:

        verbose_name_plural="COUNTRY"
        db_table = 'country_tb'
        verbose_name="COUNTRY"

    def __unicode__(self):
        return self.country_name

class CountyTb(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    country_name = models.ForeignKey(CountryTb, db_column='country_name',limit_choices_to={'active': True})
    county_name = models.CharField(max_length=100,unique=True)
    active = models.BooleanField(default=True)

    class Meta:

        verbose_name_plural="COUNTY"
        db_table = 'county_tb'
        verbose_name="COUNTY"
    def __unicode__(self):
        return self.county_name

class Disttab(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    country_name = models.ForeignKey(CountryTb, db_column='country_name',limit_choices_to={'active': True})
    county_name = models.ForeignKey(CountyTb, db_column='county_name',limit_choices_to={'active': True})
    district_name = models.CharField(unique=True, max_length=100)
    active = models.BooleanField(default=True)

    class Meta:

        verbose_name_plural="DISTRICT"
        verbose_name="DISTRICT"
        #db_table = 'district_tb'
        db_table = 'district_new'

    def __unicode__(self):
        return self.district_name

class SubdistrictTab(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    country = models.ForeignKey(CountryTb, db_column='country',limit_choices_to={'active': True})
    county = models.ForeignKey(CountyTb, db_column='county',limit_choices_to={'active': True})
    district = models.ForeignKey(Disttab, db_column='district',limit_choices_to={'active': True})
    subdistrict = models.CharField(unique=True, max_length=100, blank=True)
    active = models.BooleanField(default=True)

    class Meta:

        verbose_name_plural="SUBDISTRICT"
        verbose_name="SUBDISTRICT"
        #db_table = 'subdistrict_tab'
        db_table = 'subdistrict_new'

    def __unicode__(self):
        return self.subdistrict

class LocationTab(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    country = models.ForeignKey(CountryTb, db_column='country')
    county = models.ForeignKey(CountyTb, db_column='county')
    district = models.ForeignKey(Disttab, db_column='district')
    subdistrict = models.ForeignKey(SubdistrictTab,db_column='subdistrict',limit_choices_to={'active': True})
    location = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    class Meta:

        verbose_name_plural="LOCATIONS"
        verbose_name="LOCATIONS"
        #db_table = 'location_tab'
        db_table = 'location_new'

    def __unicode__(self):
        return self.location

class HealthCenters(models.Model):
    #id = models.IntegerField(primary_key=True)
    hospital_name = models.CharField(max_length=200)
    hospital_type = models.CharField(max_length=200)
    hospital_address = models.CharField(max_length=200)
    country_name = models.ForeignKey(CountryTb, db_column='country_name',limit_choices_to={'active': True})
    county_name = models.ForeignKey(CountyTb, db_column='county_name',null=True,limit_choices_to={'active': True})
    district_name = models.ForeignKey(Disttab, db_column='district_name',null=True,limit_choices_to={'active': True})
    subdistrict_name = models.ForeignKey(SubdistrictTab, db_column='subdistrict_name',null=True,limit_choices_to={'active': True})
    #location = models.CharField(max_length=200)
    parent_hospital = models.CharField(max_length=200)
    villages = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    class Meta:

        #db_table = 'health_centers'
        verbose_name_plural="HEALTH CENTERS"
        verbose_name="HEALTH CENTERS"
        db_table = 'health_centers_new'

    def __unicode__(self):
        return self.hospital_name

class AppConfiguration(models.Model):
    TEMP = (("celsius","Celsius"),
            ("fahrenheit","Fahrenheit"))
    IS_HIGHRISK = (('TB', 'TB'),
               ('Hypertension', 'Hypertension'),
               ('Heart-related-diseases', 'Heart-related-diseases'),
               ('Diabetes', 'Diabetes'))
    #id = models.IntegerField(primary_key=True)  # AutoField?
    country_name = models.ForeignKey(CountryTb, db_column='country_name',limit_choices_to={'active': True}, unique=True)
    wife_age_min = models.PositiveIntegerField(help_text="Enter min age in years")
    wife_age_max = models.PositiveIntegerField(help_text="Enter max age in years")
    husband_age_min = models.PositiveIntegerField(help_text="Enter min age in years")
    husband_age_max = models.PositiveIntegerField(help_text="Enter max age in years")
    temperature_units = models.CharField(max_length=20,choices=TEMP)
    escalation_schedule = models.IntegerField(help_text="Enter escalation units as number of minutes (Eg: for 2hrs =120)")
    is_highrisk = MultiSelectField(choices=IS_HIGHRISK)
    #configuration = models.TextField(max_length=480)

    class Meta:

        db_table = 'app_configuration'
        verbose_name_plural="APP CONFIGURATION"
        verbose_name="APP CONFIGURATION"

    def __unicode__(self):
        return u'for %s' %self.country_name

class AncDue(models.Model):
    # id = models.IntegerField(unique=True)
    entityid = models.CharField(primary_key=True, max_length=200)
    patientnum = models.CharField(max_length=200, blank=True)
    anmnum = models.CharField(max_length=200, blank=True)
    visittype = models.CharField(max_length=200, blank=True)
    visitno = models.IntegerField(blank=True, null=True)
    lmpdate = models.CharField(max_length=200, blank=True)
    womenname = models.CharField(max_length=200, blank=True)
    visitdate = models.CharField(max_length=200, blank=True)
    anmid = models.CharField(max_length=200, blank=True)

    class Meta:

        db_table = 'anc_due'

class FormFields(models.Model):
    FORMS = (("anc_registration","ANC Registration"),
             ("ec_registration","EC Registration"),
             ("pnc_registration","PNC Registration"),
             ("fp_registration","FP Registration"),
             ("child_registration","child Registration"))
    #id = models.IntegerField(primary_key=True)  # AutoField?
    country = models.ForeignKey(CountryTb, db_column='country')
    form_name = models.CharField(max_length=50, choices=FORMS)
    field1 = models.CharField(max_length=50, blank=True)
    field2 = models.CharField(max_length=50, blank=True)
    field3 = models.CharField(max_length=50, blank=True)
    field4 = models.CharField(max_length=50, blank=True)
    field5 = models.CharField(max_length=50, blank=True)

    class Meta:

        unique_together = ("country", "form_name",)
        db_table = "form_fields"
        verbose_name_plural="FORM FIELDS"
        verbose_name="FORM FIELDS"
    
    def __unicode__(self):
        field = str(self.form_name).replace("_"," ")
        return '%s form' %(field)

class VisitConfiguration(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    anc_visit1_from_week = models.IntegerField(blank=True, null=True)
    anc_visit1_to_week = models.IntegerField(blank=True, null=True)
    anc_visit2_from_week = models.IntegerField(blank=True, null=True)
    anc_visit2_to_week = models.IntegerField(blank=True, null=True)
    anc_visit3_from_week = models.IntegerField(blank=True, null=True)
    anc_visit3_to_week = models.IntegerField(blank=True, null=True)
    anc_visit4_from_week = models.IntegerField(blank=True, null=True)
    anc_visit4_to_week = models.IntegerField(blank=True, null=True)
    class Meta:

        db_table = 'visit_configuration'
        verbose_name_plural="VISIT CONFIGURATION"
        verbose_name="VISIT CONFIGURATION"

class AppReporting(models.Model):
    visitentityid = models.CharField(max_length=50, blank=True, null=True)
    entityidec = models.CharField(max_length=50)
    patient_name = models.CharField(max_length=100)
    anm_id = models.CharField(max_length=25)
    activity = models.CharField(max_length=25)
    indicators = models.CharField(max_length=50, blank=True, null=True)
    indicator_count = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    child_weight = models.IntegerField(blank=True, null=True)
    other_date = models.CharField(max_length=50, blank=True, null=True)
    visit_location = models.CharField(max_length=50, blank=True, null=True)
    dob = models.CharField(max_length=200, blank=True, null=True)

    class Meta:

        db_table = 'app_reporting'


class AnnualTarget(models.Model):
    YEARS = ((y,y) for y in range(2016,2100))
    anm = models.ForeignKey('UserMasters', db_column='anm', blank=True, null=True, limit_choices_to={"user_role":"ANM"})
    indicators = models.CharField(max_length=25, blank=True, null=True,choices=settings.INDICATORS)
    target = models.IntegerField()
    year = models.IntegerField(blank=True, null=True, choices=YEARS)

    class Meta:

        db_table = 'annual_target'
        verbose_name_plural="ANNUAL TARGET"
        verbose_name="ANNUAL TARGET"
