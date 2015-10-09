from django.test import TestCase
from Masters.models import *
# from django.test import Client
# from .import views

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
        print directions.directions
        print len(directions.directions)
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
        self.assertEqual(drug.drug_name,'corex')
        self.assertEqual(drug.frequency.number_of_times,'daily')
        self.assertEqual(drug.dosage.dosage,'500mg')
        self.assertEqual(drug.direction.directions,'before breakfast')
        self.assertNotEqual(drug.anc_conditions,'pallor')
        self.assertNotEqual(drug.pnc_conditions,'Blurred Vision')
        self.assertNotEqual(drug.child_illness,'Cough')
        self.assertEqual(len(drug.drug_name),5) 

class DrugApi(TestCase):
    def test_create_investigator(self):
        response = self.client.get("/druginfo/")
        self.failUnlessEqual(response.status_code, 200)

class InvestigationsTestCase(TestCase):
    def test_investigation(self):
        investigation = Investigations.objects.create(service_group_name="Radiology",investigation_name="minor dressing")
        self.assertEqual(investigation.service_group_name,'Radiology')

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
        self.subcenter = hospital = HealthCenters.objects.create(country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,hospital_name="yashoda",hospital_type="subcenter",hospital_address="begumpet",parent_hospital="appolo",villages="kukatpalli")
    def test_usermasters(self):
        users = UserMasters.objects.create(user_role="ANM",user_id="anm",name="sudheer",password="sudheer",confirm_password="sudheer",phone_number="9494022013",email="sudheer.s@dhanuhsinfotech.net",subcenter=self.subcenter,villages="YPL",lastname="sandi",hospital=self.hospital,county=self.county,country=self.country,district=self.district,subdistrict=self.subdistrict)
        self.assertEqual(users.user_role,'ANM')

class AuthApi(TestCase):
    def test_create_investigator(self):
        user = 'anm'
        password="sudheer"
        response = self.client.get("/auth/", data={'userid': user,'pwd': password})
        self.failUnlessEqual(response.status_code, 200)

class AncDueTestCase(TestCase):
    def setUp(self):
        anc = AncDue.objects.create(entityid="1234568",patientnum="9494022013",anmnum="8121337675",visittype="anc_visit",visitno="1",lmpdate="2015-07-25",womenname="sandya",visitdate="2015-10-17",anmid="anm111")
        self.assertEqual(anc.womenname,'sandya')
        self.assertEqual(len(anc.womenname),6)
