from django.test import TestCase
from Masters.models import *
from django.test import Client
from Masters.views import *

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
        self.assertEqual(drug.drug_name,'corex')
        self.assertEqual(drug.frequency.number_of_times,'daily')
        self.assertEqual(drug.dosage.dosage,'500mg')
        self.assertEqual(drug.direction.directions,'before breakfast')
        self.assertNotEqual(drug.anc_conditions,'pallor')
        self.assertNotEqual(drug.pnc_conditions,'Blurred Vision')
        self.assertNotEqual(drug.child_illness,'Cough')
        self.assertEqual(len(drug.drug_name),5) 

class DrugApi(TestCase):
    def test_druginfo(self):
        response = self.client.get("/druginfo/")
        self.failUnlessEqual(response.status_code, 200)

class VitalApi(TestCase):
    def test_vitalsdata(self):
    	visit = "123hkjqhdbkjash"
        response = self.client.get("/vitalsdata/",data={'visitid': visit})
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
        visitid = "visitid"
        entityid = "entityid"
        patientname = "patientname"
        response = self.client.get("/doctor_refer/",data={'doc_id': doc_id,'visitid': visitid,'entityid': entityid,'patientname': patientname})
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
#Workfromhere
class AuthApi(TestCase):
    def test_auth(self):
        user = 'anm'
        password="sudheer"
        response = self.client.get("/auth/", data={'userid': user,'password': password})
        self.failUnlessEqual(response.status_code, 200)

class DocApi(TestCase):
    def test_docinfo(self):
        user = 'anm'
        password="sudheer"
        response = self.client.get("/docinfo/", data={'doc_name': user,'pwd': password})
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

class SubdistrictTabApi(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        #self.hospitals_name = HealthCenters.objects.filter(county_name=county_obj,hospital_type='County',active=True).values_list('hospital_name')
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

class LoginTestCase(TestCase):
    def test_login(self):
        response = self.client.get('/admin/')
        self.assertRedirects(response, '/admin/login/?next=/admin/')

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
        hospital_name=HealthCenters.objects.create(hospital_name="testhospital",hospital_type="subcenter",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,villages="dsfjkjk",parent_hospital="parent",active=True)
        active=True
        response = self.client.get("/saveusermaintenance/",
                                   data={'country_name':self.country,'county_name':self.county,'district_name':self.district,
                                         'subdistrict_name':self.subdistrict,'village':self.village,'userrole':userrole,'userid':userid,
                                         'first_name':first_name,'last_name':last_name,'password':password,'mobile':mobile,'email':email,
                                         'subcenter_name':hospital_name,"hospitals":hospital_name,'active':active

        })
        self.failUnlessEqual(response.status_code, 200)

class SaveHealthCentersAPI(TestCase):
    def test_login(self):
        hospital_name="ou"
        hostype="subcenter"
        address="test"
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        self.village = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
        parent_hos="test"
        active=True
        response = self.client.get("/savehospital/",
                                   data={'hos_country':self.country,'hos_county':self.county,'hos_district':self.district,
                                         'hos_subdistrict':self.subdistrict,'villages':self.village,'name':hospital_name,'active':active,
                                         'type':hostype,'add':address,'parent_hos':parent_hos

        })
        self.failUnlessEqual(response.status_code, 200)

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
        # self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="SampleDistrict")
        response = self.client.get("/savedistrict/", data={'country':self.country,'county':self.county,'district':'SampleDistrict','active':True})
        self.failUnlessEqual(response.status_code, 200)

class SaveSubDistrictApi(TestCase):
    def test_save_district(self):
        self.country=CountryTb.objects.create(country_name="Sample")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="SampleCounty")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="SampleDistrict")
        response = self.client.get("/savesubdistrict/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':"SampleSub",'active':True})
        self.failUnlessEqual(response.status_code, 200)

class SaveLocationApi(TestCase):
    def test_save_district(self):
        self.country=CountryTb.objects.create(country_name="Sample")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="SampleCounty")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="SampleDistrict123")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhfasdas")
        response = self.client.get("/savelocation/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'location':"TestLocation",'active':True})
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
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        self.location = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
    def test_subcenter(self):
        response = self.client.get("/subcenter/", data={'location':self.location})
        self.failUnlessEqual(response.status_code, 200)

class ParentHospitalApi(TestCase):
    def test_parenthos_detail(self):
        hos_type = 'Subcenter'
        self.country=CountryTb.objects.create(country_name="India")
        self.county=CountyTb.objects.create(country_name=self.country,county_name="fdsfjk")
        self.district = Disttab.objects.create(country_name=self.country,county_name=self.county,district_name="fsdfkg")
        self.subdistrict = SubdistrictTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict="ksljdjhf")
        #self.village = LocationTab.objects.create(country=self.country,county=self.county,district=self.district,subdistrict=self.subdistrict,location="dsfjkjk")
        #hospital_name=HealthCenters.objects.create(hospital_name="testhospital",hospital_type="subcenter",hospital_address="testaddress",country_name=self.country,county_name=self.county,district_name=self.district,subdistrict_name=self.subdistrict,villages="dsfjkjk",parent_hospital="parent",active=True)
        response = self.client.get("/parenthospital/", data={'country':self.country,'county':self.county,'district':self.district,'subdistrict':self.subdistrict,'hos_type':hos_type})
        self.failUnlessEqual(response.status_code, 200)

class ResetpasswordApi(TestCase):
    def test_reser_password(self):
        response = self.client.get("/resetpassword/", data={'resetpassword':'123456'})
        self.failUnlessEqual(response.status_code, 200)