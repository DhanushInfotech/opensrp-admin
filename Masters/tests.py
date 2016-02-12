from django.test import TestCase
from django.test import TestCase
from Masters.models import *
from django.test import Client
from Masters.views import *
import json

class CountryTbTestCase(TestCase):
    def setUp(self):
    	CountryTb.objects.create(country_name="India", country_code="91")
    def test_country(self):
    	country = CountryTb.objects.get(country_name="India")
    	code = CountryTb.objects.get(country_code="91")
    	self.assertEqual(country.country_name,'India')
        self.assertEqual(code.country_code,'91')
        self.assertEqual(len(country.country_name),5)

class CountyTbTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
    def test_county(self):
        county = CountyTb.objects.create(country_name=self.country,county_name="andhra")
        self.assertEqual(county.country_name.country_name,'India')
        self.assertEqual(len(county.county_name),6)

class DisttabTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="andhra")
    def test_district(self):
        district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="Prakasam")
        self.assertEqual(district.district_name,'Prakasam')
        self.assertEqual(len(district.district_name),8)


class SubdistrictTabTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="andhra")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="Prakasam")
    def test_subdistrict(self):
        subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ongole")
        self.assertEqual(subdistrict.subdistrict,'ongole')

class LocationTabTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="andhra")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="Prakasam")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ongole")
    def test_location(self):
        locations = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="chirch center")
        self.assertEqual(locations.location,'chirch center')


class HealthCentersTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="andhra")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="Prakasam")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ongole")
    def test_healthcenters(self):
        hospital = HealthCenters.objects.create(country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,hospital_name="yashoda",hospital_type="subcenter",hospital_address="begumpet",parent_hospital="appolo",villages="kukatpalli")
        self.assertEqual(hospital.hospital_name,'yashoda',hospital.country_name)  
        self.assertNotEqual(hospital.hospital_name,'yashodasfd')
        self.assertEqual(hospital.hospital_address,'begumpet')
        self.assertEqual(hospital.hospital_type,'subcenter')
        self.assertEqual(hospital.villages,'kukatpalli',hospital.district_name)
        self.assertNotEqual(hospital.villages,'kukatpallisss',hospital.subdistrict_name)
        self.assertEqual(len(hospital.villages),10)

class AppConfigurationTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
    def test_appconfiguration(self):
    	configuration = AppConfiguration.objects.create(country_name=self.country,wife_age_min="18",wife_age_max="60",husband_age_min="25",husband_age_max="74",temperature_units="celsius",escalation_schedule="2")
    	self.assertEqual(configuration.wife_age_max,'60')
    	self.assertNotEqual(configuration.wife_age_min,'35')

class ICD10TestCase(TestCase):
    def setUp(self):
        ICD10.objects.create(ICD10_Chapter="dhanush",ICD10_Code="1245",ICD10_Name="nurse")
    def test_icd10(self):
        ICD10_Chapter = ICD10.objects.get(ICD10_Chapter="dhanush")
        ICD10_Code = ICD10.objects.get(ICD10_Code="1245")
        ICD10_Name = ICD10.objects.get(ICD10_Name="nurse")
        self.assertEqual(ICD10_Chapter.ICD10_Chapter,'dhanush')
        self.assertEqual(ICD10_Code.ICD10_Code,'1245')
        self.assertEqual(ICD10_Name.ICD10_Name,'nurse')
        self.assertEqual(len(ICD10_Name.ICD10_Name),5)

class DirectionsTestCase(TestCase):
    def setUp(self):
        Directions.objects.create(directions="before breakfast")
    def test_directions(self):
        directions = Directions.objects.get(directions="before breakfast")
        self.assertEqual(directions.directions,'before breakfast')
        self.assertEqual(len(directions.directions),16)

class DosageTestCase(TestCase):
    def setUp(self):
        Dosage.objects.create(dosage="500mg")
    def test_dosage(self):
        dosage = Dosage.objects.get(dosage="500mg")
        self.assertEqual(dosage.dosage,'500mg')
        self.assertEqual(len(dosage.dosage),5)

class FrequencyTestCase(TestCase):
    def setUp(self):
        Frequency.objects.create(number_of_times="daily")
    def test_frequency(self):
        frequency = Frequency.objects.get(number_of_times="daily")
        self.assertEqual(frequency.number_of_times,'daily')
        self.assertEqual(len(frequency.number_of_times),5)

class DrugInfoTestCase(TestCase):
    def setUp(self):
        self.direction=Directions.objects.create(directions="before breakfast")
        self.dosage=Dosage.objects.create(dosage="500mg")
        self.frequency=Frequency.objects.create(number_of_times="daily")
    def test_druginfo(self):
        drug=DrugInfo.objects.create(drug_name="corex",frequency=self.frequency,dosage=self.dosage,direction=self.direction,anc_conditions="pallor",pnc_conditions="Blurred Vision",child_illness="Cough")
        drug = DrugInfo.objects.all()[0]
        self.assertEquals(drug.direction,self.direction)
        self.assertEqual(drug.drug_name,'corex')
        self.assertEqual(drug.frequency.number_of_times,'daily')
        self.assertEqual(drug.dosage.dosage,'500mg')
        self.assertEqual(drug.direction.directions,'before breakfast')
        self.assertNotEqual(drug.anc_conditions,'pallor')
        self.assertNotEqual(drug.pnc_conditions,'Blurred Vision')
        self.assertNotEqual(drug.child_illness,'Cough')
        self.assertEqual(len(drug.drug_name),5) 


class DrugAPITestCase(TestCase):
    def setUp(self):
        self.direction=Directions.objects.create(directions="before breakfast")
        self.dosage=Dosage.objects.create(dosage="500mg")
        self.frequency=Frequency.objects.create(number_of_times="daily")
        self.icd10=ICD10.objects.create(ICD10_Chapter="dhanush",ICD10_Code="1245",ICD10_Name="nurse")
    def test_druginfo(self):
        drug=DrugInfo.objects.create(drug_name="corex",frequency=self.frequency,dosage=self.dosage,direction=self.direction,anc_conditions="pallor",pnc_conditions="Blurred Vision",child_illness="Cough")
        icd10=ICD10.objects.create(ICD10_Chapter="dhanush",ICD10_Code="1245",ICD10_Name="nurse")
        investigation = Investigations.objects.create(service_group_name="Radiology",investigation_name="minor dressing")
        response = self.client.get("/druginfo/")
        self.failUnlessEqual(response.status_code, 200)
        drug = DrugInfo.objects.all()[0]
        icd=ICD10.objects.all()[0]
        self.assertEquals(drug.direction,self.direction)
        self.assertEquals(icd10.ICD10_Name,"nurse")
        self.assertEquals(investigation.service_group_name,"Radiology")


class VitalApi(TestCase):
    def test_vitalsdata(self):
    	visit = "123hkjqhdbkjash"
        visitNumber={'name':'ancVisitNumber','value':12}
        ancVisit={'name':'ancVisitDate','value':'10/10/2016'}
        response = self.client.get("/vitalsdata/",data={'visit': "0663b5b4-49a5-4e48-bece-f88094a44c52"})
        response = self.client.get("/vitalsdata/",data={'visit': "5c1fc968-6e9d-49b0-905e-c22e13b88cb0"})
        self.failUnlessEqual(response.status_code, 200)

class DocoverviewApi(TestCase):
    def test_docoverview(self):
    	o_visitid = "123hkjqhdbkjash"
    	o_entityid = "adjashkdhaskjd"
        response = self.client.get("/docoverview/",data={'o_visitid': o_visitid,'o_entityid':o_entityid})
        self.failUnlessEqual(response.status_code, 200)

class DocReferApi(TestCase):
    def test_doctor_refer(self):
        doc_id="docid"
        visitid = "0663b5b4-49a5-4e48-bece-f88094a44c52"
        entityid = "f3d77a5a-8c51-4f44-817f-acf7c821118f"
        patientname = "patientname"
        userrole="DOC"
        userid="test123"
        first_name="test"
        last_name="unit"
        password="123456"
        mobile="123456789"
        email="a@b.com"
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        self.village = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
        self.hospital_name=HealthCenters.objects.create(hospital_name="testhospital",hospital_type="PHC",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,parent_hospital="subdistricthospital",active=True)
        self.subdistrict_hospital_name=HealthCenters.objects.create(hospital_name="subdistricthospital",hospital_type="SubDistrict",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,parent_hospital="districthospital",active=True)
        self.district_hospital_name=HealthCenters.objects.create(hospital_name="districthospital",hospital_type="District",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,parent_hospital="countyhospital",active=True)
        self.county_hospital_name=HealthCenters.objects.create(hospital_name="countyhospital",hospital_type="County",hospital_address="testaddress",country_name=self.country,county_name=self.county,parent_hospital="countryhospital",active=True)
        self.country_hospital_name=HealthCenters.objects.create(hospital_name="countryhospital",hospital_type="Country",hospital_address="testaddress",country_name=self.country,parent_hospital="parent",active=True)
        active=True
        user=UserMasters.objects.create(user_role="DOC",user_id=userid,name=first_name,password=password,
                                   phone_number=mobile,email=email,hospital=self.hospital_name,lastname=last_name,
                                   county=self.county,country=self.country,district=self.district,subdistrict=self.subdistrict)
        subdistrictuser=UserMasters.objects.create(user_role="DOC",user_id="subdistrictdoc",name=first_name,password=password,
                                   phone_number=mobile,email=email,hospital=self.subdistrict_hospital_name,lastname=last_name,
                                   county=self.county,country=self.country,district=self.district,subdistrict=self.subdistrict)
        districtuser=UserMasters.objects.create(user_role="DOC",user_id="districtdoc",name=first_name,password=password,
                           phone_number=mobile,email=email,hospital=self.district_hospital_name,lastname=last_name,
                           county=self.county,country=self.country,district=self.district)
        countyuser=UserMasters.objects.create(user_role="DOC",user_id="countydoc",name=first_name,password=password,
                           phone_number=mobile,email=email,hospital=self.county_hospital_name,lastname=last_name,
                           county=self.county,country=self.country)
        countryuser=UserMasters.objects.create(user_role="DOC",user_id="countrydoc",name=first_name,password=password,
                           phone_number=mobile,email=email,hospital=self.country_hospital_name,lastname=last_name,
                           country=self.country)
        poc_data = PocInfo.objects.create(visitentityid="0663b5b4-49a5-4e48-bece-f88094a44c52",entityidec="f3d77a5a-8c51-4f44-817f-acf7c821118f",phc="testhospital")
        poc_data = PocInfo.objects.create(visitentityid="5c1fc968-6e9d-49b0-905e-c22e13b88cb0",entityidec="ddd5e997-10d2-4d2d-8606-9012c1db0061",phc="testhospital")
        poc_data = PocInfo.objects.create(visitentityid="db22c1b0-2059-4c32-a1b5-2b9e5d121e42",entityidec="ddd5e997-10d2-4d2d-8606-9012c1db0061",phc="testhospital")
        poc_data = PocInfo.objects.create(visitentityid="fc2beeea-2fab-4eb0-b92c-17a807b53926",entityidec="b99e9350-b7a4-4038-a4b2-11cea4b9a851",phc="testhospital")
        response = self.client.get("/doctor_refer/",data={'docid': userid,'visitid': visitid,'entityid': entityid,'patientname': patientname})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/doctor_refer/",data={'docid': "subdistrictdoc",'visitid': visitid,'entityid': entityid,'patientname': patientname})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/doctor_refer/",data={'docid': "districtdoc",'visitid': visitid,'entityid': entityid,'patientname': patientname})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/doctor_refer/",data={'docid': "countydoc",'visitid': visitid,'entityid': entityid,'patientname': patientname})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/docoverview/",data={'visitid': visitid,'entityid': entityid})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/docoverview/",data={"visitid":"5c1fc968-6e9d-49b0-905e-c22e13b88cb0","entityid":"ddd5e997-10d2-4d2d-8606-9012c1db0061"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/docoverview/",data={"visitid":"db22c1b0-2059-4c32-a1b5-2b9e5d121e42","entityid":"ddd5e997-10d2-4d2d-8606-9012c1db0061"})
        self.failUnlessEqual(response.status_code, 200)

class FormFieldsTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
    def test_formfields(self):
        form = FormFields.objects.create(form_name="Anc Registration",country=self.country,field1="A",field2="B",field3="C",field4="D",field5="E")
        self.assertEqual(form.form_name,'Anc Registration',form.country)

class UserMastersTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="Pakistan")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="andhra")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="Prakasam")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ongole")
        self.hospital = HealthCenters.objects.create(country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,hospital_name="yashoda",hospital_type="subcenter",hospital_address="begumpet",parent_hospital="appolo",villages="kukatpalli")
        self.subcenter = HealthCenters.objects.create(country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,hospital_name="yashoda",hospital_type="subcenter",hospital_address="begumpet",parent_hospital="appolo",villages="kukatpalli")
    def test_usermasters(self):
        users = UserMasters.objects.create(user_role="ANM",user_id="anm",name="sudheer",password="sudheer",confirm_password="sudheer",phone_number="9494022013",email="sudheer.s@dhanuhsinfotech.net",subcenter=self.subcenter,villages="YPL",lastname="sandi",hospital=self.hospital,county=self.county,country=self.country,district=self.district,subdistrict=self.subdistrict)
        self.assertEqual(users.user_role,'ANM')
    def test_annual_target(self):
        users = UserMasters.objects.create(user_role="ANM",user_id="TestAnm123",name="sudheer",password="sudheer",confirm_password="sudheer",phone_number="9494022013",email="sudheer.s@dhanuhsinfotech.net",subcenter=self.subcenter,villages="YPL",
                                           lastname="sandi",hospital=self.hospital,county=self.county,country=self.country,
                                           district=self.district,subdistrict=self.subdistrict)
        AnnualTarget.obj

    def test_app_reporting(self):
        visitentityid = "0663b5b4-49a5-4e48-bece-f88094a44c52"
        entityidec = "f3d77a5a-8c51-4f44-817f-acf7c821118f"
        patient_name = "Test patient"
        users = UserMasters.objects.create(user_role="ANM",user_id="TestAnm",name="sudheer",password="sudheer",confirm_password="sudheer",phone_number="9494022013",email="sudheer.s@dhanuhsinfotech.net",subcenter=self.subcenter,villages="YPL",
                                           lastname="sandi",hospital=self.hospital,county=self.county,country=self.country,
                                           district=self.district,subdistrict=self.subdistrict)
        anm_id = "TestAnm"
        activity = "anc"
        #indicator = "asdasdsa"
        indicator_count = 0
        date = "2016-02-01"
        location = "Chemoinoi"
        child_weight = 0
        visit_date = "2016-01-10"
        visit_location = "elsewhere"
        child_dob = "2015-11-23"
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                                     anm_id=anm_id,activity=activity,indicators="candom",indicator_count=1,
                                     date=date,location=location,child_weight=child_weight,other_date=visit_date,
                                     visit_location=visit_location,dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                                     anm_id=anm_id,activity=activity,indicators="tt1",indicator_count=1,
                                     date=date,location=location,child_weight=child_weight,other_date=visit_date,
                                     visit_location=visit_location,dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                                     anm_id=anm_id,activity=activity,indicators="tt2",indicator_count=1,
                                     date=date,location=location,child_weight=child_weight,other_date=visit_date,
                                     visit_location=visit_location,dob=child_dob)


        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="pnc",indicators="cesarean",indicator_count=0,
                             date=date,location=location,child_weight=child_weight,other_date=visit_date,
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="pnc",indicators="cesarean",indicator_count=0,
                             date=date,location=location,child_weight=child_weight,other_date=visit_date,
                             visit_location="dh",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="pnc",indicators="cesarean",indicator_count=0,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="pnc",indicators="cesarean",indicator_count=0,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="dh",dob=child_dob)

        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="FP",indicators="condom",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date=visit_date,
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="FP",indicators="ecp",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date=visit_date,
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="FP",indicators="iud",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date=visit_date	,
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="FP",indicators="condom",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="FP",indicators="ecp",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="FP",indicators="iud",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="child",indicators="bcg opv_0 hepb_0 pentavalent_1 BF",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="child_illness",indicators="diarrhea_dehydration",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)

        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="Mortality",indicators="anctopnc_MaternalDeath",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="Mortality",indicators="anc_MaternalDeath",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)
        AppReporting.objects.create(visitentityid=visitentityid,entityidec=entityidec,patient_name=patient_name,
                             anm_id=anm_id,activity="Mortality",indicators="pnc_MaternalDeath",indicator_count=4,
                             date=date,location=location,child_weight=child_weight,other_date="2015-04-23",
                             visit_location="chc",dob=child_dob)
        report = AppReporting.objects.get(indicators="tt1")
        self.assertEquals(report.anm_id,"TestAnm")
        #activity=ANC&anmid=anm111
        response = self.client.get("/reporting/", data={"activity":"ANC","anmid":"TestAnm"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/reporting/", data={"activity":"PREGNANCY","anmid":"TestAnm"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/reporting/", data={"activity":"FP","anmid":"TestAnm"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/reporting/", data={"activity":"child","anmid":"TestAnm"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/reporting/", data={"activity":"mortality","anmid":"TestAnm"})
        self.failUnlessEqual(response.status_code, 200)

class AuthApi(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="Pakistan",country_code="92")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="andhra")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="Prakasam")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ongole")
        self.hospital = HealthCenters.objects.create(country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,hospital_name="yashoda",hospital_type="Subcenter",hospital_address="begumpet",parent_hospital="appolo",villages="kukatpalli")
        self.subcenter = HealthCenters.objects.create(country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,hospital_name="yashoda",hospital_type="Subcenter",hospital_address="begumpet",parent_hospital="appolo",villages="kukatpalli")
        self.phc_hospital_name=HealthCenters.objects.create(hospital_name="authphc",hospital_type="PHC",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,parent_hospital="subdistricthospital",active=True)
    def test_auth(self):
        configuration = AppConfiguration.objects.create(country_name=self.country,wife_age_min="18",wife_age_max="60",husband_age_min="25",husband_age_max="74",temperature_units="celsius",escalation_schedule="2")
        form = FormFields.objects.create(form_name="anc_registration",country=self.country,field1="A",field2="B",field3="C",field4="D",field5="E")
        form = FormFields.objects.create(form_name="pnc_registration",country=self.country,field1="A",field2="B",field3="C",field4="D",field5="E")
        form = FormFields.objects.create(form_name="ec_registration",country=self.country,field1="A",field2="B",field3="C",field4="D",field5="E")
        form = FormFields.objects.create(form_name="fp_registration",country=self.country,field1="A",field2="B",field3="C",field4="D",field5="E")
        form = FormFields.objects.create(form_name="child_registration",country=self.country,field1="A",field2="B",field3="C",field4="D",field5="E")
        users = UserMasters.objects.create(user_role="ANM",user_id="anm",name="anm",password="9305a83381280d88e2364062056f385314db03d1",confirm_password="9305a83381280d88e2364062056f385314db03d1",phone_number="9494022013",email="sudheer.s@dhanuhsinfotech.net",subcenter=self.subcenter,villages="YPL",lastname="sandi",hospital=self.hospital,county=self.county,country=self.country,district=self.district,subdistrict=self.subdistrict)
        self.direction=Directions.objects.create(directions="before breakfast")
        self.dosage=Dosage.objects.create(dosage="500mg")
        self.frequency=Frequency.objects.create(number_of_times="daily")
        drug=DrugInfo.objects.create(drug_name="corex",frequency=self.frequency,dosage=self.dosage,direction=self.direction,anc_conditions="pallor",pnc_conditions="Blurred Vision",child_illness="Cough")
        response = self.client.get("/auth/", data={'userid': 'anm','pwd': 'sudheer'})
        self.failUnlessEqual(response.status_code, 200)
        doc_users = UserMasters.objects.create(user_role="DOC",user_id="doc",name="doc",password="9305a83381280d88e2364062056f385314db03d1",confirm_password="9305a83381280d88e2364062056f385314db03d1",phone_number="9494022013",email="sudheer.s@dhanuhsinfotech.net",lastname="sandi",hospital=self.phc_hospital_name,county=self.county,country=self.country,district=self.district,subdistrict=self.subdistrict)
        response = self.client.get("/auth/", data={'userid': 'doc','pwd': 'sudheer'})
        self.failUnlessEqual(response.status_code, 200)

class DocApi(TestCase):
    def test_docinfo(self):
        userrole="DOC"
        userid="test123"
        first_name="test"
        last_name="unit"
        password="123456"
        mobile="123456789"
        email="a@b.com"
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        self.village = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
        self.hospital_name=HealthCenters.objects.create(hospital_name="testhospital",hospital_type="PHC",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,parent_hospital="parent",active=True)
        active=True
        user=UserMasters.objects.create(user_role="DOC",user_id=userid,name=first_name,password=password,
                                   phone_number=mobile,email=email,hospital=self.hospital_name,lastname=last_name,
                                   county=self.county,country=self.country,district=self.district,subdistrict=self.subdistrict)
        poc_data = PocInfo.objects.create(visitentityid="0663b5b4-49a5-4e48-bece-f88094a44c52",entityidec="f3d77a5a-8c51-4f44-817f-acf7c821118f",phc="testhospital")
        poc_data = PocInfo.objects.create(visitentityid="5c1fc968-6e9d-49b0-905e-c22e13b88cb0",entityidec="ddd5e997-10d2-4d2d-8606-9012c1db0061",phc="testhospital")
        poc_data = PocInfo.objects.create(visitentityid="db22c1b0-2059-4c32-a1b5-2b9e5d121e42",entityidec="ddd5e997-10d2-4d2d-8606-9012c1db0061",phc="testhospital")
        poc_data = PocInfo.objects.create(visitentityid="fc2beeea-2fab-4eb0-b92c-17a807b53926",entityidec="b99e9350-b7a4-4038-a4b2-11cea4b9a851",phc="testhospital")
        response = self.client.get("/docinfo/", data={'docname': userid,'pwd': password})
        self.failUnlessEqual(response.status_code, 200)


class AncDueTestCase(TestCase):
    def setUp(self):
        anc = AncDue.objects.create(entityid="1234568",patientnum="9494022013",anmnum="8121337675",visittype="anc_visit",visitno="1",lmpdate="2015-07-25",womenname="sandya",visitdate="2015-10-17",anmid="anm111")
        self.assertEqual(anc.womenname,'sandya')
        self.assertEqual(len(anc.womenname),6)
  
class SendSmsApi(TestCase):
    def test_sendsms(self):
        phone_number = "9494022013"
        msg = "Poc is given to the patient"
        response = self.client.get("/sendsms/", data={'phone_number': phone_number,'msg': msg })        
        self.failUnlessEqual(response.status_code, 200)

class CountyApi(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="NW")
        self.country_hospital_name=HealthCenters.objects.create(hospital_name="CountryHospital",hospital_type="Country",hospital_address="testaddress",country_name=self.country,parent_hospital="parent",active=True)
    def test_county(self):
        response = self.client.get("/county/", data={'country_name':self.country})
        self.failUnlessEqual(response.status_code, 200)

class DisttabApi(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
    def test_district(self):
        response = self.client.get("/district/", data={'country_name':self.country,'county_name':self.county,'district_name':self.district})
        self.failUnlessEqual(response.status_code, 200)
        print

class SubdistrictTabApi(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
    def test_subdistrict(self):
        response = self.client.get("/subdistrict/", data={'country_name':self.country,'county_name':self.county,'district_name':self.district,'subdistrict_name':self.subdistrict})
        self.failUnlessEqual(response.status_code, 200)

class LocationApi(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        self.location = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
    def test_location(self):
        response = self.client.get("/location/", data={'country_name':self.country,'county_name':self.county,'district_name':self.district,'subdistrict_name':self.subdistrict,'location_name':self.location})
        self.failUnlessEqual(response.status_code, 200)

class LocationsApi(TestCase):
    def test_location(self):
        response = self.client.get("/location/")
        self.failUnlessEqual(response.status_code, 200)

class SaveUserMaintenanceAPI(TestCase):
    def test_login(self):
        userrole="ANM"
        userid="test123"
        first_name="test"
        last_name="unit"
        password="123456"
        mobile="123456789"
        email="a@b.com"
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        self.village = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
        hospital_name=HealthCenters.objects.create(hospital_name="testhospital",hospital_type="Subcenter",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,villages="dsfjkjk",parent_hospital="parent",active=True)
        self.hospital_name=HealthCenters.objects.create(hospital_name="PHCHospital",hospital_type="PHC",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,parent_hospital="subdistricthospital",active=True)
        self.subdistrict_hospital_name=HealthCenters.objects.create(hospital_name="SubDistrictHospital",hospital_type="SubDistrict",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,parent_hospital="districthospital",active=True)
        self.district_hospital_name=HealthCenters.objects.create(hospital_name="DistrictHospital",hospital_type="District",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,parent_hospital="countyhospital",active=True)
        self.county_hospital_name=HealthCenters.objects.create(hospital_name="CountyHospital",hospital_type="County",hospital_address="testaddress",country_name=self.country,county_name=self.county,parent_hospital="countryhospital",active=True)
        self.country_hospital_name=HealthCenters.objects.create(hospital_name="CountryHospital",hospital_type="Country",hospital_address="testaddress",country_name=self.country,parent_hospital="parent",active=True)
        active="true"
        response = self.client.get("/saveusermaintenance/",
                                   data={'country_name':self.country,'county_name':self.county,'district_name':self.district,
                                         'subdistrict_name':self.subdistrict,'village':self.village,'userrole':userrole,'userid':userid,
                                         'first_name':first_name,'last_name':last_name,'password':password,'mobile':mobile,'email':email,
                                         'subcenter_name':hospital_name,"hospitals":hospital_name,'active':active

        })
        self.failUnlessEqual(response.status_code, 200)
        user = UserMasters.objects.all()[0]
        self.assertEquals(user.country,self.country)

        response = self.client.get("/saveusermaintenance/",
                                   data={'country_name':self.country,'county_name':self.county,'district_name':self.district,
                                         'subdistrict_name':self.subdistrict,'village':self.village,'userrole':"DOC",'userid':"phcdoc",
                                         'first_name':first_name,'last_name':last_name,'password':password,'mobile':mobile,'email':email,
                                         "hospitals":self.hospital_name,'active':active

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/saveusermaintenance/",
                                   data={'country_name':self.country,'county_name':self.county,'district_name':self.district,
                                         'subdistrict_name':self.subdistrict,'village':self.village,'userrole':"DOC",'userid':"subdoc",
                                         'first_name':first_name,'last_name':last_name,'password':password,'mobile':mobile,'email':email,
                                         "hospitals":self.subdistrict_hospital_name,'active':active

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/saveusermaintenance/",
                                   data={'country_name':self.country,'county_name':self.county,'district_name':self.district,
                                         'village':self.village,'userrole':"DOC",'userid':"disdoc",
                                         'first_name':first_name,'last_name':last_name,'password':password,'mobile':mobile,'email':email,
                                         "hospitals":self.district_hospital_name,'active':active

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/saveusermaintenance/",
                                   data={'country_name':self.country,'county_name':self.county,
                                         'village':self.village,'userrole':"DOC",'userid':"countydoc",
                                         'first_name':first_name,'last_name':last_name,'password':password,'mobile':mobile,'email':email,
                                         "hospitals":self.county_hospital_name,'active':active

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/saveusermaintenance/",
                                   data={'country_name':self.country,
                                         'village':self.village,'userrole':"DOC",'userid':"countrydoc",
                                         'first_name':first_name,'last_name':last_name,'password':password,'mobile':mobile,'email':email,
                                         "hospitals":self.country_hospital_name,'active':active

        })
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get("/updateusermaintenance/",
                                   data={'country_name':self.country,'county_name':self.county,'district_name':self.district,
                                         'subdistrict_name':self.subdistrict,'village':self.village,'userrole':userrole,'userid':userid,
                                         'first_name':first_name,'last_name':last_name,'password':password,'mobile':mobile,'email':email,
                                         'subcenter_name':hospital_name,"hospitals":hospital_name,'active':active

        })
        self.failUnlessEqual(response.status_code, 200)

class SaveHealthCentersAPI(TestCase):
    def test_login(self):
        hospital_name="ou"
        hostype="Subcenter"
        address="test"
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        self.village = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
        parent_hos="test"
        active="true"
        response = self.client.get("/savehospital/",
                                   data={'hos_country':self.country,
                                         'name':"TestCountry",'active':active,
                                         'type':'Country','add':address

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/savehospital/",
                                   data={'hos_country':self.country,'hos_county':self.county,
                                         'name':"TestCounty",'active':active,
                                         'type':'County','add':address,'parent_hos':"TestCountry"

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/savehospital/",
                                   data={'hos_country':self.country,'hos_county':self.county,'hos_district':self.district,
                                         'villages':self.village,'name':"TestDistrict",'active':active,
                                         'type':'District','add':address,'parent_hos':"TestCounty"

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/savehospital/",
                                   data={'hos_country':self.country,'hos_county':self.county,'hos_district':self.district,
                                         'hos_subdistrict':self.subdistrict,'villages':self.village,'name':"TestSubDistrict",'active':active,
                                         'type':'SubDistrict','add':address,'parent_hos':"TestDistrict"

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/savehospital/",
                                   data={'hos_country':self.country,'hos_county':self.county,'hos_district':self.district,
                                         'hos_subdistrict':self.subdistrict,'villages':self.village,'name':"TestPHC",'active':active,
                                         'type':'PHC','add':address,'parent_hos':"TestSubDistrict"

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/savehospital/",
                                   data={'hos_country':self.country,'hos_county':self.county,'hos_district':self.district,
                                         'hos_subdistrict':self.subdistrict,'villages':self.village,'name':hospital_name,'active':active,
                                         'type':hostype,'add':address,'parent_hos':"TestPHC"

        })
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get("/updatehospital/",
                                   data={'hos_country':"India",
                                         'name':"TestCountry123",'hos_county':"null",'hos_district':"null",
                                         'hos_subdistrict':"null",'villages':self.village,'active':active,
                                         'type':'Country','add':address

        })
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/updatehospital/",
                                   data={'hos_country':"India",
                                         'name':"TestCountry123",'hos_county':"fdsfjk",'hos_district':"null",
                                         'hos_subdistrict':"null",'villages':self.village,'active':active,
                                         'type':'County','add':address

        })
        self.failUnlessEqual(response.status_code, 200)

class DataList(TestCase):
    data_list('a',['a','b','c'])

class ParentHosptal(TestCase):
    parent_hospital('a',['a','b','c'])
    parent_hospital('null',['a','b','c'])

class HospitalValidateApi(TestCase):

    def test_hospital_validate(self):
        response = self.client.get("/hospitalvalidate/", data={'hname':'testhospital','id':123456})
        self.failUnlessEqual(response.status_code, 200)

class LocationValidateApi(TestCase):
    def setUp(self):
        self.country = CountryTb.objects.create(country_name="india")

    def test_location_validate(self):
        response = self.client.get("/locationvalidate/", data={'lname':'testhospital','id':123456,'country_name':self.country})
        self.failUnlessEqual(response.status_code, 200)

class SaveDistrictApi(TestCase):
    def test_save_district(self):
        self.country=CountryTb.objects.create(country_name="Sample")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="SampleCounty")
        response = self.client.get("/savedistrict/", data={'country':self.country,'county':self.county,'district':'SampleDistrict','active':"true"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/updatedistrict/", data={'country':self.country,'county':self.county,'district':'SampleDistrictedited','active':"true"})
        self.failUnlessEqual(response.status_code, 200)

class SaveSubDistrictApi(TestCase):
    def test_save_district(self):
        self.country=CountryTb.objects.create(country_name="Sample")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="SampleCounty")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="SampleDistrict")
        response = self.client.get("/savesubdistrict/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':"SampleSub",'active':"true"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/updatesubdistrict/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':"SampleSubedited",'active':"true"})
        self.failUnlessEqual(response.status_code, 200)

class SaveLocationApi(TestCase):
    def test_save_district(self):
        self.country=CountryTb.objects.create(country_name="Sample")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="SampleCounty")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="SampleDistrict123")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhfasdas")
        response = self.client.get("/savelocation/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'location':"TestLocation",'active':True})
        self.failUnlessEqual(response.status_code, 200)
        location = LocationTab.objects.all()
        self.assertEquals(location.count(), 1)
        response = self.client.get("/updatelocation/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'location':"TestLocationedited",'active':True})
        self.failUnlessEqual(response.status_code, 200)

class SubdistrictValidateApi(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
    def test_subdistirct_validate(self):
        response = self.client.get("/subdistrictvalidate/", data={'sname':'sacho','id':123456,'subdistrict':self.subdistrict})
        self.failUnlessEqual(response.status_code, 200)

class DistrictValidate(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
    def test_district_validate(self):
        response = self.client.get("/districtvalidate/", data={'dname':'dulla','id':123456,'district_name':self.district})

class UserValidateApi(TestCase):
    def test_user_validate(self):
        response = self.client.get("/uservalidate/", data={'uname':'sudheer','id':123456})
        self.failUnlessEqual(response.status_code, 200)

class SavePasswordApi(TestCase):
    def test_save_password(self):
        response = self.client.get("/savepassword/", data={'password':'14525968','id':123456})
        self.failUnlessEqual(response.status_code, 200)

class SubcenterApi(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="SZ")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="Hyderabad")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="SRNagar")
        self.location = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="BKGuda")
        hospital_name=HealthCenters.objects.create(hospital_name="testhospitalsub",hospital_type="Subcenter",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,villages="BKGuda",parent_hospital="parent",active=True)
    def test_subcenter(self):
        response = self.client.get("/subcenter/", data={'location':"testhospitalsub"})
        self.failUnlessEqual(response.status_code, 200)

class ParentHospitalApi(TestCase):
    def test_parenthos_detail(self):
        hos_type = 'Subcenter'
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        self.village = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
        self.Subcenter_hospital_name=HealthCenters.objects.create(hospital_name="newsubcenterhospital",hospital_type="Subcenter",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,villages=self.village,parent_hospital="parent",active=True)
        self.phc_hospital_name=HealthCenters.objects.create(hospital_name="newPHCHospital",hospital_type="PHC",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,parent_hospital="subdistricthospital",active=True)
        self.subdistrict_hospital_name=HealthCenters.objects.create(hospital_name="newSubDistrictHospital",hospital_type="SubDistrict",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,parent_hospital="districthospital",active=True)
        self.district_hospital_name=HealthCenters.objects.create(hospital_name="newDistrictHospital",hospital_type="District",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,parent_hospital="countyhospital",active=True)
        self.county_hospital_name=HealthCenters.objects.create(hospital_name="newCountyHospital",hospital_type="County",hospital_address="testaddress",country_name=self.country,county_name=self.county,parent_hospital="countryhospital",active=True)
        self.country_hospital_name=HealthCenters.objects.create(hospital_name="newCountryHospital",hospital_type="Country",hospital_address="testaddress",country_name=self.country,active=True)
        response = self.client.get("/parenthospital/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'hos_type':hos_type})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/parenthospital/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'hos_type':"PHC"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/parenthospital/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'hos_type':"SubDistrict"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/parenthospital/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'hos_type':"District"})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/parenthospital/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'hos_type':"County"})
        self.failUnlessEqual(response.status_code, 200)


class ResetpasswordApi(TestCase):
    def test_reser_password(self):
        response = self.client.get("/resetpassword/", data={'resetpassword':'123456'})
        self.failUnlessEqual(response.status_code, 200)

class DocSMSTest(TestCase):
    def test_docsms(self):
        wph="9985408792"
        pph="9550726256"
        wsms="testw"
        psms="sms p"
        docsms(workerph=wph,patientph=pph,worker_sms=wsms,patientsms=psms)

class POCUpdateTest(TestCase):
    def test_poc_update(self):
        visit_id = "0663b5b4-49a5-4e48-bece-f88094a44c52"
        entity_id = "f3d77a5a-8c51-4f44-817f-acf7c821118f"
        document_id="380b0e1a64b294e8294cbb55c5086ea5"
        doctor_id="unittest"
        pending="unittest"
        patient_ph="123456789"
        patient_name="test"
        poc_data = "%7B%22investigations%22%3A%5B%22laboratory-Blood+Test+for+Human+immunodeficiency+virus+%28HIV%29+antibody%22%5D%2C%22planofCareDate%22%3A%2204-11-2015%22%2C%22drugs%22%3A%5B%7B%22dosage%22%3A%2235+ml%22%2C%22frequency%22%3A%22Every+12+Hours%22%2C%22drugNoOfDays%22%3A%226%22%2C%22drugQty%22%3A%228%22%2C%22direction%22%3A%22before+break+fast%22%2C%22drugName%22%3A%22Protein+and+Fatty+Acid+Supplement%22%7D%5D%2C%22diagnosis%22%3A%5B%22O07.5+-+Other+and+unspecified+failed+attempted+abortion%2C+complicated+by+genital+tract+and+pelvic+infection%22%5D%2C%22visitNumber%22%3A%221%22%2C%22doctorName%22%3A%22neha%22%2C%22advice%22%3A%22my+advice%22%2C%22documentId%22%3A%22c04214947963000c8d8d4e7f9e6cbeca%22%2C%22visitType%22%3A%22ANC%22%7D"
        response = self.client.get("/pocupdate/", data={'visitid':visit_id,'entityid':entity_id,'docid':document_id,'doctorid':doctor_id,
                                                        'pending':pending,'patientph':patient_ph,'patientname':patient_name,
                                                        'pocinfo':'{"investigations":"Test blood"}'})
        self.failUnlessEqual(response.status_code, 200)

class VisitConfigurationTest(TestCase):
    def setUp(self):
    	VisitConfiguration.objects.create(anc_visit1_from_week=4, anc_visit1_to_week=6,anc_visit2_from_week=8, anc_visit2_to_week=10,
                                          anc_visit3_from_week=12, anc_visit3_to_week=14,anc_visit4_from_week=16, anc_visit4_to_week=18)
    def test_visit_conf(self):
        visit = VisitConfiguration.objects.get(anc_visit1_from_week=4)
        self.assertEquals(visit.anc_visit1_to_week,6)
