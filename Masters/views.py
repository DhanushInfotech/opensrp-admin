from django.shortcuts import render
from Masters.models import *
from django.http import HttpResponse
import json
from collections import defaultdict
import time
from datetime import date, timedelta,datetime
from django.shortcuts import render_to_response
from Masters.forms import *
from django.core.context_processors import csrf
from django.conf import settings
from django.db import connection
from django.db.models import Q

def druginfo(request):
    all_info=defaultdict(list)
    drug_details = DrugInfo.objects.all().values_list('drug_name','frequency__number_of_times','dosage__dosage','direction__directions')
    for drug in drug_details:
        drug_data = {}
        drug_data['name']=drug[0]
        drug_data['frequency'] = str(drug[1])
        drug_data['dosage']=drug[2]
        drug_data['direction']=drug[3]
        all_info['drug_data'].append(drug_data)
    diagnosis = ICD10.objects.filter(can_select='True',status='True').values_list('ICD10_Chapter','ICD10_Code','ICD10_Name')
    for d in diagnosis:
        diagnosis_data={}
        diagnosis_data['ICD10_Chapter']=d[0]
        diagnosis_data['ICD10_Code']=d[1]
        diagnosis_data['ICD10_Name']=d[2]
        all_info['diagnosis_data'].append(diagnosis_data)
    investigation_info = Investigations.objects.filter(is_active=True).values_list('service_group_name','investigation_name')
    for investigation in investigation_info:
        investigation_data = {}
        investigation_data['service_group_name'] = investigation[0]
        investigation_data['investigation_name'] = investigation[1]
        all_info['investigation_data'].append(investigation_data)
    result_json = json.dumps(all_info)
    return HttpResponse(result_json)

def poc_update(request):
    patientph="9985408792"
    if request.method =="GET":
        document_id=request.GET.get("docid","")
        poc_info=request.GET.get("pocinfo","")
        visitid=request.GET.get("visitid","")
        entityid=request.GET.get("entityid","")
        docid=request.GET.get("doctorid","")
        pending =request.GET.get("pending","")
        patientph =str(request.GET.get("patientph",""))
        patientname =str(request.GET.get("patientname",""))
    elif request.method =="POST":
        document_id=request.POST.get("docid","")
        poc_info=request.POST.get("pocinfo","")
        visitid=request.POST.get("visitid","")
        entityid=request.POST.get("entityid","")
        docid=request.POST.get("doctorid","")
        pending =request.POST.get("pending","")
        patientph =request.GET.get("patientph","")
    poc_details = json.loads(poc_info)
    poc = []
    poc_data = {}
    server_version = int(round(time.time() * 1000))
    poc_data['pending']=pending
    poc_data['poc'] = str(poc_info)
    poc_data['server_version'] = server_version
    poc_backup_data = json.dumps(poc_data)
    #Getting old poc and will update that with present value at the end
    visit_backup = PocBackup.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).values_list('poc','id')
    if len(visit_backup)>0:
        for visit in visit_backup:
            old_poc= json.loads(visit[0])
            poc.append(old_poc)
        #del_poc_bckup=PocBackup.objects.filter(id = int(visit_backup[0][1])).delete()
    poc_backup = PocBackup(visitentityid=str(visitid),entityidec=str(entityid),docid=str(docid),poc=poc_backup_data)
    poc_backup.save()
    #Reading all values from document
    #pront
    result = {}
    entity_detail="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_id/?key=%22"+str(document_id)+"%22"
    poc_output=commands.getoutput(entity_detail)
    poutput=json.loads(poc_output)
    form_ins= poutput['rows'][0]['value'][2]
    row_data = poutput['rows'][0]['value'][2]['formInstance']['form']['fields']
    #Updating docPocInfo with pending reason or poc
    for i in range((len(row_data))):
        row = row_data[i]
        if 'name' in row.keys():
            if str(row['name']) == 'docPocInfo':
                poc.append(poc_data)
                poc_json = json.dumps(poc)
                row['value']=poc_json
                row_data[i]=row
    #Creating new document with latest docPocInfo
    result["_id"]=str(form_ins["_id"])
    result["_rev"]=str(form_ins["_rev"])
    result["anmId"]=str(form_ins["anmId"])
    anmId=str(form_ins["anmId"])
    result["clientVersion"]=str(form_ins["clientVersion"])
    result["entityId"]=str(form_ins["entityId"])
    result["formDataDefinitionVersion"]=str(form_ins["formDataDefinitionVersion"])
    result["formInstance"]=form_ins["formInstance"]
    result["formName"]=str(form_ins["formName"])
    result["instanceId"]=str(form_ins["instanceId"])
    result["serverVersion"]=server_version
    result["type"]=str(form_ins["type"])
    ord_result = json.dumps(result)
    poc_doc_update_curl = "curl -vX PUT http://202.153.34.169:5984/drishti-form/%s -d '''%s'''" %(str(document_id),ord_result)
    poc_doc_update=commands.getoutput(poc_doc_update_curl)

    if len(pending)>0:
        update_poc=PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).update(pending=str(pending),docid=str(docid))
    #Updating backup table with latest poc/pending status info
    visit_info = PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).values_list('visitentityid','entityidec')
    if len(pending)==0:
        anm_details = UserMasters.objects.filter(user_id=str(anmId)).values_list('phone_number','country__country_name')
        anm_country = str(anm_details[0][1])
        anm_phone = str(anm_details[0][0])
        patient_sms = "Dear %s your prescription " %patientname
        if len(poc_details["investigations"]) > 0:
            patient_sms+=" Investigations: "
            for investigation in poc_details["investigations"]:
                patient_sms = patient_sms+investigation
        if len(poc_details["drugs"]) > 0:
            patient_sms+=" drugs: "
            for drugs in poc_details["drugs"]:
                patient_sms = patient_sms+drugs["drugName"]+drugs["direction"]+drugs["frequency"]+drugs["drugQty"]+drugs["drugNoOfDays"]
        if len(poc_details["diagnosis"]) > 0:
            patient_sms+=" diagnosis: "
            for diagnosis in poc_details["diagnosis"]:
                patient_sms = patient_sms+diagnosis
        anm_sms = "POC is given for %s on" %patientname
        anm_sms+=datetime.now().strftime('%d-%b-%Y %H:%M:%S')
        country_code= str(CountryTb.objects.filter(country_name=str(anm_country)).values_list('country_code')[0][0])
        anm_phone = country_code+anm_phone[-int(settings.PHONE_NUMBER_LENGTH):]
        patient_phone = country_code+patientph[-int(settings.PHONE_NUMBER_LENGTH):]
        anm_sms,patient_sms = docsms(workerph=anm_phone,patientph=patient_phone,worker_sms=anm_sms,patientsms=patient_sms)
        del_poc = PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).delete()
    return HttpResponse(json.dumps({"status":"success"}))

def docsms(workerph=None,patientph=None,worker_sms=None,patientsms=None):
    anm_sms_var = '{"phone":["tel:'+str(workerph)+'"], "text":"' +worker_sms+'"}'
    anm_sms_curl= 'curl -i -H "Authorization: Token 78ffc91c6a5287d7cc7a9a68c4903cc61d87aecb" -H "Content-type: application/json"  -H "Accept: application/json" POST -d'+ "'"+anm_sms_var+"'"+' http://202.153.34.174/api/v1/messages.json '
    anm_sms_output = commands.getoutput(anm_sms_curl)
    patient_sms=str(patientsms)
    patient_sms_var = '{"phone":["tel:'+str(patientph)+'"], "text":"' +patient_sms+'"}'
    patient_sms_curl= 'curl -i -H "Authorization: Token 78ffc91c6a5287d7cc7a9a68c4903cc61d87aecb" -H "Content-type: application/json"  -H "Accept: application/json" POST -d'+ "'"+patient_sms_var+"'"+' http://202.153.34.174/api/v1/messages.json '
    patient_sms_output = commands.getoutput(patient_sms_curl)
    return anm_sms_output,patient_sms_output

def docinfo(request):
    if request.method == "GET":
        doc_name= request.GET.get('docname',"")
        password = request.GET.get('pwd',"")
    elif request.method == "POST":
        doc_name= request.GET.get('docname',"")
        password = request.GET.get('pwd',"")
    end_res = '{}'

    doc_loc = UserMasters.objects.filter(user_id=str(doc_name),user_role="DOC").values_list('hospital__hospital_name')
    if len(doc_loc)>0:
    	doc_loc = str(doc_loc[0][0]).replace(" (PHC)","")
    else:
    	return HttpResponse('{"status":"Invalid username/password"}')
    resultdata=defaultdict(list)
    display_result=[]
    entity_list = PocInfo.objects.filter(phc=doc_loc).values_list('visitentityid','entityidec','pending','docid').distinct()
    if len(entity_list) == 0:
    	return HttpResponse(json.dumps(display_result))
    for entity in entity_list:
        if str(entity[2])!='None':
            if len(entity[2])>1 and str(doc_name) != str(entity[3]):
                continue
    	entity_detail_id=str(entity[1])
        ancvisit_detail="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_EntityId?key=%22"+str(entity[0])+"%22&descending=true"
        visit_output = commands.getoutput(ancvisit_detail)
        visit_data1 = json.loads(visit_output)
        row = visit_data1['rows']
        visit_data=[]
        poc_len=1
        doc_con='no'
        visit={}
        newvisitdata=defaultdict(list)
        newvisit={}

        field_data = row[-1]['value'][1]['form']['fields']
        for f in range((len(field_data)-1),-1,-1):
            fd = field_data[f]
            if 'name' in fd.keys():
                if fd['name'] == 'docPocInfo':
                    poc_len=len(fd['value'])
                elif fd['name'] == 'isConsultDoctor':
                    doc_con = fd['value']
        if doc_con == 'yes':
            #-----------------PNC DATA --------------
            if row[-1]['value'][0] == 'pnc_visit' or row[-1]['value'][0] == 'pnc_visit_edit':
                doc_id=row[-1]['id']
                for visitdata in row:
                    pnc_tags = ["pncNumber","pncVisitDate","difficulties1","difficulties2","abdominalProblems","urineStoolProblems",
                                "hasFeverSymptoms","breastProblems","vaginalProblems","bpSystolic","bpDiastolic","temperature","pulseRate",
                                "bloodGlucoseData","weight","anmPoc","pncVisitPlace","pncVisitDate","isHighRisk","hbLevel"]
                    f = lambda x: x[0].get("value") if len(x)>0 else ""
                    fetched_dict = copyf(visitdata["value"][1]["form"]["fields"],"name",pnc_tags)
                    visit["pncNumber"]=f(copyf(fetched_dict,"name","pncNumber"))
                    visit["pncVisitDate"]=f(copyf(fetched_dict,"name","pncVisitDate"))
                    visit["difficulties1"]=f(copyf(fetched_dict,"name","difficulties1"))
                    visit["difficulties2"]=f(copyf(fetched_dict,"name","difficulties2"))
                    visit["abdominalProblems"]=f(copyf(fetched_dict,"name","abdominalProblems"))
                    visit["urineStoolProblems"]=f(copyf(fetched_dict,"name","urineStoolProblems"))
                    visit["hasFeverSymptoms"]=f(copyf(fetched_dict,"name","hasFeverSymptoms"))
                    visit["breastProblems"]=f(copyf(fetched_dict,"name","breastProblems"))
                    visit["vaginalProblems"]=f(copyf(fetched_dict,"name","vaginalProblems"))
                    visit["bpSystolic"]=f(copyf(fetched_dict,"name","bpSystolic"))
                    visit["bpDiastolic"]=f(copyf(fetched_dict,"name","bpDiastolic"))
                    visit["temperature"]=f(copyf(fetched_dict,"name","temperature"))
                    visit["pulseRate"]=f(copyf(fetched_dict,"name","pulseRate"))
                    visit["bloodGlucoseData"]=f(copyf(fetched_dict,"name","bloodGlucoseData"))
                    visit["weight"]=f(copyf(fetched_dict,"name","weight"))
                    visit["anmPoc"]=f(copyf(fetched_dict,"name","anmPoc"))
                    visit["pncVisitPlace"]=f(copyf(fetched_dict,"name","pncVisitPlace"))
                    visit["pncVisitDate"]=f(copyf(fetched_dict,"name","pncVisitDate"))
                    visit["isHighRisk"]=f(copyf(fetched_dict,"name","isHighRisk"))
                    visit["hbLevel"]=f(copyf(fetched_dict,"name","hbLevel"))
                    visit['visit_type'] = 'PNC'
                    visit["entityid"] = entity[0]
                    visit['id']=doc_id
                visit_data.append(visit)

            elif row[-1]['value'][0] == 'anc_visit' or row[-1]['value'][0] == 'anc_visit_edit':
                doc_id=row[-1]['id']
                for visitdata in row:
                    anc_tags = ["ancVisitNumber","ancNumber","ancVisitPerson","ancVisitDate","riskObservedDuringANC","bpSystolic","bpDiastolic",
                                "temperature","pulseRate","bloodGlucoseData","weight","anmPoc","isHighRisk","fetalData"]
                    f = lambda x: x[0].get("value") if len(x)>0 else ""
                    fetched_dict = copyf(visitdata["value"][1]["form"]["fields"],"name",anc_tags)
                    visit["ancVisitNumber"]=f(copyf(fetched_dict,"name","ancVisitNumber"))
                    visit["ancNumber"]=f(copyf(fetched_dict,"name","ancNumber"))
                    visit["ancVisitPerson"]=f(copyf(fetched_dict,"name","ancVisitPerson"))
                    visit["ancVisitDate"]=f(copyf(fetched_dict,"name","ancVisitDate"))
                    visit["riskObservedDuringANC"]=f(copyf(fetched_dict,"name","riskObservedDuringANC"))
                    visit["bpSystolic"]=f(copyf(fetched_dict,"name","bpSystolic"))
                    visit["bpDiastolic"]=f(copyf(fetched_dict,"name","bpDiastolic"))
                    visit["temperature"]=f(copyf(fetched_dict,"name","temperature"))
                    visit["pulseRate"]=f(copyf(fetched_dict,"name","pulseRate"))
                    visit["bpSystolic"]=f(copyf(fetched_dict,"name","bpSystolic"))
                    visit["bpDiastolic"]=f(copyf(fetched_dict,"name","bpDiastolic"))
                    visit["temperature"]=f(copyf(fetched_dict,"name","temperature"))
                    visit["pulseRate"]=f(copyf(fetched_dict,"name","pulseRate"))
                    visit["bloodGlucoseData"]=f(copyf(fetched_dict,"name","bloodGlucoseData"))
                    visit["weight"]=f(copyf(fetched_dict,"name","weight"))
                    visit["anmPoc"]=f(copyf(fetched_dict,"name","anmPoc"))
                    visit["isHighRisk"]=f(copyf(fetched_dict,"name","isHighRisk"))
                    visit["fetalData"]=f(copyf(fetched_dict,"name","fetalData"))
                    visit['visit_type'] = 'ANC'
                    visit["entityid"] = entity[0]
                    visit['id']=doc_id
                visit_data.append(visit)
            elif row[-1]['value'][0] == 'child_illness' or row[-1]['value'][0] == 'child_illness_edit':
                doc_id=row[-1]['id']
                for childdata in row:
                    child_tags = ["dateOfBirth","childSigns","childSignsOther","immediateReferral","immediateReferralReason","reportChildDiseaseDate","reportChildDisease","reportChildDiseaseOther"
                                ,"reportChildDiseasePlace","childTemperature","numberOfORSGiven","childReferral","anmPoc","isHighRisk","submissionDate","id","numberOfDaysCough","breathsPerMinute","daysOfDiarrhea","bloodInStool","vommitEveryThing","daysOfFever","sickVisitDate"]
                    f = lambda x: x[-1].get("value") if len(x)>0 else ""
                    fetched_dict = copyf(childdata["value"][1]["form"]["fields"],"name",child_tags)
                    visit["dateOfBirth"]=f(copyf(fetched_dict,"name","dateOfBirth"))
                    visit["childSigns"]=f(copyf(fetched_dict,"name","childSigns"))
                    visit["childSignsOther"]=f(copyf(fetched_dict,"name","childSignsOther"))
                    visit["immediateReferral"]=f(copyf(fetched_dict,"name","immediateReferral"))
                    visit["immediateReferralReason"]=f(copyf(fetched_dict,"name","immediateReferralReason"))
                    visit["reportChildDisease"]=f(copyf(fetched_dict,"name","reportChildDisease"))
                    visit["reportChildDiseaseOther"]=f(copyf(fetched_dict,"name","reportChildDiseaseOther"))
                    visit["reportChildDiseaseDate"]=f(copyf(fetched_dict,"name","reportChildDiseaseDate"))
                    visit["reportChildDiseasePlace"]=f(copyf(fetched_dict,"name","reportChildDiseasePlace"))
                    visit["childTemperature"]=f(copyf(fetched_dict,"name","childTemperature"))
                    visit["numberOfORSGiven"]=f(copyf(fetched_dict,"name","numberOfORSGiven"))
                    visit["childReferral"]=f(copyf(fetched_dict,"name","childReferral"))
                    visit["numberOfDaysCough"]=f(copyf(fetched_dict,"name","numberOfDaysCough"))
                    visit["breathsPerMinute"]=f(copyf(fetched_dict,"name","breathsPerMinute"))
                    visit["daysOfDiarrhea"]=f(copyf(fetched_dict,"name","daysOfDiarrhea"))
                    visit["bloodInStool"]=f(copyf(fetched_dict,"name","bloodInStool"))
                    visit["vommitEveryThing"]=f(copyf(fetched_dict,"name","vommitEveryThing"))
                    visit["daysOfFever"]=f(copyf(fetched_dict,"name","daysOfFever"))
                    visit["sickVisitDate"]=f(copyf(fetched_dict,"name","sickVisitDate"))
                    visit["anmPoc"]=f(copyf(fetched_dict,"name","anmPoc"))
                    visit["isHighRisk"]=f(copyf(fetched_dict,"name","isHighRisk"))
                    visit["submissionDate"]=f(copyf(fetched_dict,"name","submissionDate"))
                    visit["id"]=doc_id
                    visit['visit_type'] = 'CHILD'
                    visit["entityid"] = entity[0]
                visit_data.append(visit)

        entity_detail="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_EntityId?key=%22"+entity_detail_id+"%22&descending=true"
        poc_output=commands.getoutput(entity_detail)
        poutput=json.loads(poc_output)
        row1 = poutput['rows']
        if len(visit_data)>0:
            result=defaultdict(list)
            if len(row1)>0:
                for i in range(len(row1)):
                    for data in row1[i]["value"][1]['form']['fields']:
                        if row1[i]['value'][0] == "anc_registration_oa" or row1[i]['value'][0]=="anc_registration" or row1[i]['value'][0]=="anc_reg_edit_oa" or row1[i]['value'][0]=="anc_reg_edit":
                            key=data.get('name')
                            value=data.get('value')
                            if key=='edd':
                                temp={}
                                temp={key:value}
                                edd_datetime = str(value).split(',')
                                edd_date = edd_datetime[-1].split(' ')
                                edd = '-'.join(edd_date[1:4])
                                if len(edd)>0:
                                    dat = datetime.strptime(edd,'%d-%b-%Y')
                                    lmp_date = dat+timedelta(days=-280)
                                    lmp = datetime.strftime(lmp_date ,'%d-%b-%Y')
                                    visit['edd']=edd
                                    visit['lmp']=lmp
                                    visit_data.append(visit)
                        elif row1[i]['value'][0] == "child_registration_oa":
                            key = data.get('name')
                            if 'value' in child_data.keys():
                                value = child_data.get('value')
                            else:
                                value=''
                            if key == 'gender':
                                visit['gender']=value
                            elif key == 'name':
                                visit['name']=value
                            elif key == 'registrationDate':
                                visit['registrationDate']=value
                            elif key == 'motherName':
                                temp={}
                                temp={"wifeName":value}
                                result.update(temp)
                            elif key == 'fatherName':
                                temp={}
                                temp={"husbandName":value}
                                result.update(temp)
                        elif row1[i]['value'][0] == "anc_close" or row1[i]['value'][0] == "pnc_close":
                            continue

                        key=data.get('name')
                        value=data.get('value')
                        if key=='wifeName':
                            temp={}
                            temp={key:value}
                            result.update(temp)
                        elif key=='wifeAge':
                            temp={}
                            temp={key:value}
                            result.update(temp)
                        elif key=='phoneNumber':
                            temp={}
                            temp={"phoneNumber":value}
                            result.update(temp)
                        elif key=='district':
                            temp={}
                            temp={key:value}
                            result.update(temp)
                        elif key=='husbandName':
                            temp={}
                            temp={key:value}
                            result.update(temp)
                        elif key=='village':
                            temp={}
                            temp={key:value}
                            result.update(temp)
                        elif key == 'aadharNumber':
                            temp={}
                            temp={key:value}
                            result.update(temp)
                    temp_list=[]
                    temp_list.append(visit_data[-1])
                    result["riskinfo"]=temp_list
                    result["entityidec"] = entity_detail_id
                    result["anmId"] = row1[0]['value'][2]
                    if str(entity[2]) == "None":
                        result["pending"]=""
                    else:
                        result["pending"]=str(entity[2])
                    display_result.append(result)
            else:
                entity_curl_child="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_EntityId?key=%22"+str(entity[0])+"%22"
                child_output = commands.getoutput(entity_curl_child)
                child_data = json.loads(child_output)
                child_rows = child_data['rows']
                for child in child_rows:
                    if str(child['value'][0])=='child_registration_oa':
                        for c in child["value"][1]['form']['fields']:
                            key = c.get('name')
                            if 'value' in c.keys():
                                value = c.get('value')
                            else:
                                value=''
                            if key == 'gender':
                                visit['gender']=value
                            elif key == 'name':
                                visit['name']=value
                            elif key == 'registrationDate':
                                visit['registrationDate']=value
                            elif key =='edd':
                                visit['edd']=value
                            elif key=='phoneNumber':
                                temp={}
                                temp={"phoneNumber":value}
                                result.update(temp)
                            elif key == 'motherName':
                                temp={}
                                temp={"wifeName":value}
                                result.update(temp)
                            elif key == 'fatherName':
                                temp={}
                                temp={"husbandName":value}
                                result.update(temp)
                            elif key=='village':
                                temp={}
                                temp={key:value}
                                result.update(temp)
                temp_list=[]
                temp_list.append(visit_data[-1])
                result["riskinfo"]=temp_list
                result["entityidec"] = entity_detail_id
                if str(entity[2]) == "None":
                    visit["pending"]=""
                else:
                    visit["pending"]=str(entity[2])
                display_result.append(result)
    end_res= json.dumps(display_result)
    return HttpResponse(end_res)

def drug_info():
    drug_result = defaultdict(list)
    diseases = settings.DISEASES
    for disease in diseases:
        drug = DrugInfo.objects.filter(Q(anc_conditions__regex=str(disease)) | Q(pnc_conditions__regex=str(disease)) | Q(child_illness__regex=str(disease))).values_list('drug_name')
        if len(drug)>0:
            for d in drug:
                drug_result[str(disease)].append(d[0])
    return dict(drug_result)

def auth(request):
    if request.method == 'GET':
        username = str(request.GET.get('userid',''))
        password = str(request.GET.get('pwd',''))
    else:
        username = str(request.POST.get('userid',''))
        password = str(request.POST.get('pwd',''))
    pwd = hashlib.sha1()
    pwd.update(password)
    password = pwd.hexdigest()
    user_details=UserMasters.objects.filter(user_id=str(username),password=password).values_list('user_role','id','name','country',)
    if len(user_details) ==0:
        return HttpResponse('{"status":"Invalid username/password"}')
    user_role=user_details[0][0]
    user_data = {}
    personal_info ={}
    personal_info['name']=user_details[0][2]
    user_data["personal_info"]=str(personal_info)
    user_data["role"] = str(user_role)
    if user_role.upper() =='DOC':
        doc_details=UserMasters.objects.filter(id=int(user_details[0][1])).values_list('country','county','district','subdistrict','hospital','phone_number','email')
        user_data["personal_info"]={"hospital":doc_details[0][4],"phone":str(doc_details[0][5]),"email":str(doc_details[0][6])}
    elif user_role.upper() == 'ANM':
        location = {}
        anm_details=UserMasters.objects.filter(id=int(user_details[0][1])).values_list('country__country_name','county__county_name','district__district_name','subdistrict__subdistrict','subcenter__hospital_name','villages','phone_number','email')
        subcenter = str(anm_details[0][4])
        country_obj = CountryTb.objects.get(country_name=str(anm_details[0][0]))
        country_code = CountryTb.objects.filter(country_name=str(anm_details[0][0])).values_list("country_code")[0][0]
        anm_phc = HealthCenters.objects.filter(hospital_name=subcenter,hospital_type='Subcenter').values_list('parent_hospital')
        phc = str(anm_phc[0][0])
        location["phcName"]=phc.replace(" ","")
        location["subCenter"]=subcenter.replace(" ","")
        location["villages"]=str(anm_details[0][5]).split(',')
        drug_details = drug_info()
        config_fields = AppConfiguration.objects.filter(country_name=str(user_details[0][3])).values_list('wife_age_min','wife_age_max','husband_age_min','husband_age_max','temperature_units','is_highrisk')
        form_fields = FormFields.objects.filter(country=str(user_details[0][3])).values_list("form_name","field1","field2","field3","field4","field5")
        if len(config_fields) >0:
            config_data = {"wifeAgeMin":config_fields[0][0],"wifeAgeMax":config_fields[0][1],"husbandAgeMin":config_fields[0][2],"husbandAgeMax":config_fields[0][3],"temperature":config_fields[0][4]}
        form_values=[]
        if len(form_fields)>0:

            for form in form_fields:
                if form[0] == "anc_registration":
                    form_lables={"ANCRegistration":[str(label) for label in form[1:] if label !=""]}
                elif form[0] == "ec_registration":
                    form_lables={"ECRegistration":[str(label) for label in form[1:] if label !=""]}
                elif form[0] == "fp_registration":
                    form_lables={"FPRegistration":[str(label) for label in form[1:] if label !=""]}
                elif form[0] == "pnc_registration":
                    form_lables={"PNCRegistration":[str(label) for label in form[1:] if label !=""]}
                elif form[0] == "child_registration":
                    form_lables={"ChildRegistration":[str(label) for label in form[1:] if label !=""]}
                form_values.append(form_lables)
        user_data["personal_info"]={"location":location,"phone":str(anm_details[0][6]),"email":str(anm_details[0][7]),"drugs":drug_details,"configuration":config_data,"countryCode":str(country_code),"formLabels":str(form_values),"isHighRisk":str(config_fields[0][5]).split(",")}
    end_res= json.dumps(user_data)
    return HttpResponse(end_res)



def vitalsdata(request):
    vital_readings=[]
    if request.method == 'GET':
        visitid = request.GET.get('visit','')
    else:
        visitid = request.POST.get('visit','')
    ancvisit_detail="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_EntityId?key=%22"+str(visitid)+"%22&descending=True"
    visit_output = commands.getoutput(ancvisit_detail)
    visit_data = json.loads(visit_output)
    visit_details = visit_data['rows']
    for visit in visit_details:
        visit_reading={}
        if visit['value'][0] == 'anc_visit':
            required_values= ['ancVisitNumber','ancVisitDate','bpSystolic','bpDiastolic','temperature','fetalData','bloodGlucoseData']
            fetched_dict = copyf(visit['value'][1]['form']['fields'],'name',required_values)
            visit_reading["visit_type"]="ANC"
            visit_reading["visit_number"]= copyf(fetched_dict,'name','ancVisitNumber')[0].get('value','0')
            visit_reading["bpSystolic"]= copyf(fetched_dict,'name','bpSystolic')[0].get('value','0')
            visit_reading["bpDiastolic"]= copyf(fetched_dict,'name','bpDiastolic')[0].get('value','0')
            visit_reading["visitDate"]= copyf(fetched_dict,'name','ancVisitDate')[0].get('value','0')
            visit_reading["temperature"]= copyf(fetched_dict,'name','temperature')[0].get('value','0')
            visit_reading["fetalData"]= copyf(fetched_dict,'name','fetalData')[0].get('value','0')
            visit_reading["bloodGlucoseData"]= copyf(fetched_dict,'name','bloodGlucoseData')[0].get('value','0')
            vital_readings.append(visit_reading)
        elif visit['value'][0] == 'pnc_visit':
            required_values= ['pncVisitDate','bpSystolic','bpDiastolic','temperature','fetalData','bloodGlucoseData']
            fetched_dict = copyf(visit['value'][1]['form']['fields'],'name',required_values)
            visit_reading["visit_type"]="PNC"
            visit_reading["bpSystolic"]= copyf(fetched_dict,'name','bpSystolic')[0].get('value','0')
            visit_reading["bpDiastolic"]= copyf(fetched_dict,'name','bpDiastolic')[0].get('value','0')
            visit_reading["visitDate"]= copyf(fetched_dict,'name','pncVisitDate')[0].get('value','0')
            visit_reading["temperature"]= copyf(fetched_dict,'name','temperature')[0].get('value','0')
            visit_reading["fetalData"]= copyf(fetched_dict,'name','fetalData')[0].get('value','0')
            visit_reading["bloodGlucoseData"]= copyf(fetched_dict,'name','bloodGlucoseData')[0].get('value','0')
            vital_readings.append(visit_reading)
    return HttpResponse(json.dumps(vital_readings))

def copyf(dictlist, key, valuelist):
      return [dictio for dictio in dictlist if dictio[key] in valuelist]

def doctor_refer(request):
    if request.method=="GET":
        doc_id=request.GET.get("docid","")
        visitid = request.GET.get("visitid","")
        entityid = request.GET.get("entityid","")
        patientname = str(request.GET.get("patientname",""))
    doc_details = UserMasters.objects.filter(user_id=str(doc_id)).values_list("hospital__hospital_name")
    if len(doc_details)==0:
    	return HttpResponse('{"status":"Invalid username/password"}')
    doc_hospital = str(doc_details[0][0]).replace(" (PHC)","")
    hospital_details = HealthCenters.objects.filter(hospital_name=doc_hospital).values_list("hospital_type")
    if str(hospital_details[0][0])=="PHC":
        level = 2
        location = str(HealthCenters.objects.filter(hospital_name=str(doc_hospital),hospital_type='PHC').values_list("parent_hospital")[0][0])
        doctor_details = UserMasters.objects.filter(hospital__hospital_name=str(location)).values_list("name","phone_number","country__country_name")
        for doctor in doctor_details:
            print doctor[2]
            country_code=str(CountryTb.objects.filter(country_name=str(doctor[2])).values_list("country_code")[0][0])
            doctor_phone=country_code+str(doctor[1])[-int(settings.PHONE_NUMBER_LENGTH):]
            msg = "Dear Doctor, %s has been referred to you for Doctor Consultation for ANC/PNC/Child Visit" %patientname
            doc_sms,junk_sms = docsms(workerph=doctor_phone,worker_sms=msg)
        update_level = PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).update(level=str(level),phc=str(location),timestamp=datetime.now())
    elif str(hospital_details[0][0])=="SubDistrict":
        level = 3
        location = HealthCenters.objects.filter(hospital_name=str(doc_details[0][0]),hospital_type='SubDistrict').values_list("parent_hospital")[0][0]
        doctor_details = UserMasters.objects.filter(hospital__hospital_name=str(location)).values_list("name","phone_number","country__country_name")
        for doctor in doctor_details:
            country_code=str(CountryTb.objects.filter(country_name=str(doctor[2])).values_list("country_code")[0][0])
            doctor_phone=country_code+str(doctor[1])[-int(settings.PHONE_NUMBER_LENGTH):]
            msg = "Dear %s has been referred to you for Doctor Consultation for ANC/PNC/Child Visit" %patientname
            doc_sms,junk_sms = docsms(workerph=doctor_phone,worker_sms=msg)
        update_level = PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).update(level=str(level),phc=str(location),timestamp=datetime.now())
    elif str(hospital_details[0][0])=="District":
        level = 4
        location = HealthCenters.objects.filter(hospital_name=str(doc_details[0][0]),hospital_type='District').values_list("parent_hospital")[0][0]
        doctor_details = UserMasters.objects.filter(hospital__hospital_name=str(location)).values_list("name","phone_number","country__country_name")
        for doctor in doctor_details:
            country_code=str(CountryTb.objects.filter(country_name=str(doctor[2])).values_list("country_code")[0][0])
            doctor_phone=country_code+str(doctor[1])[-int(settings.PHONE_NUMBER_LENGTH):]
            msg = "Dear %s has been referred to you for Doctor Consultation for ANC/PNC/Child Visit" %patientname
            doc_sms,junk_sms = docsms(workerph=doctor_phone,worker_sms=msg)
        update_level = PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).update(level=str(level),phc=str(location),timestamp=datetime.now())
    elif str(hospital_details[0][0])=="County":
        level = 2
        location = HealthCenters.objects.filter(hospital_name=str(doc_details[0][0]),hospital_type='County').values_list("parent_hospital")[0][0]
        doctor_details = UserMasters.objects.filter(hospital__hospital_name=str(location)).values_list("name","phone_number","country__country_name")
        for doctor in doctor_details:
            country_code=str(CountryTb.objects.filter(country_name=str(doctor[2])).values_list("country_code")[0][0])
            doctor_phone=country_code+str(doctor[1])[-int(settings.PHONE_NUMBER_LENGTH):]
            msg = "Dear %s has been referred to you for Doctor Consultation for ANC/PNC/Child Visit" %patientname
            doc_sms,junk_sms = docsms(workerph=doctor_phone,worker_sms=msg)
        update_level = PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).update(level=str(level),phc=str(location),timestamp=datetime.now())

    return HttpResponse('Level upgraded')

def sendsms(request):
    if request.method == "GET":
        phone_num = request.GET.get("tel","")
        msg = str(request.GET.get("message",""))
    sms_var = '{"phone":'+str(phone_num)+', "text":' +msg+'}'
    sms_curl= 'curl -i -H "Authorization: Token 78ffc91c6a5287d7cc7a9a68c4903cc61d87aecb" -H "Content-type: application/json"  -H "Accept: application/json" POST -d'+ "'"+sms_var+"'"+' http://202.153.34.174/api/v1/messages.json '
    sms_output = commands.getoutput(sms_curl)
    return HttpResponse('SMS sent')


def admin_hospital(request):
    countryname = CountryTb.objects.filter(active=True).values_list('country_name')
    country_name=[]
    for n in countryname:
        country_name.append(n[0])

    c = {}
    c.update(csrf(request))
    return render_to_response('addhospital1.html',{'x':country_name,'csrf_token':c['csrf_token']})

def get_hospital(request):
    if request.method == "GET":
        type_name= request.GET.get('devata',"")

    elif request.method == "POST":
        type_name= request.GET.get('devata',"")

    if str(type_name) == 'district':
        address = DimLocation.objects.all().values_list('district').distinct()
    elif str(type_name) == 'taluka':
        address = DimLocation.objects.all().values_list('taluka').distinct()
    elif str(type_name) == 'phc':
        address = DimLocation.objects.all().values_list('phc__name').distinct()
    elif str(type_name) == 'subcenter':
        address = DimLocation.objects.all().values_list('subcenter').distinct()

    res = []
    for a in address:
        res.append(str(a[0]))
    result = {'res':res}
    res = json.dumps(result)
    return HttpResponse(res)

def save_hospital(request):
    if request.method == 'GET':
        hos_name = request.GET.get('name','')
        hostype = request.GET.get('type','')
        address = request.GET.get('add','')
        country = request.GET.get('hos_country','')
        county = request.GET.get('hos_county','')
        district =request.GET.get('hos_district','')
        subdistrict =request.GET.get('hos_subdistrict','')
        # location =request.GET.get('hos_location','')
        villages = request.GET.get('hos_village','')
        parenthos = request.GET.get('parent_hos','')
        active=request.GET.get('active','')
    elif request.method == 'POST':
        hos_name = request.POST.get('name','')
        hostype = request.POST.get('type','')
        address = request.POST.get('add','')
        country = request.POST.get('hos_country','')
        county = request.POST.get('hos_county','')
        district =request.POST.get('hos_district','')
        subdistrict =request.POST.get('hos_subdistrict','')
        # location =request.POST.get('hos_location','')
        villages = request.POST.get('hos_village','')
        parenthos = request.POST.get('parent_hos','')
        active=request.POST.get('active','')
    status = 0
    if str(active) == 'true':
        status = 1
    if len(villages) == 0:
        villages = ''
    country_obj = CountryTb.objects.get(country_name=str(country))
    county_obj=''
    district_obj=''
    subdistrict_obj=''
    if len(county)==0:
        # county_obj = CountyTb.objects.get(county_name=str(county))
        hospital_details = HealthCenters(hospital_name=str(hos_name),hospital_type=str(hostype),hospital_address=str(address),country_name=country_obj,active=status)
        hospital_details.save()
        x = {"result":'/admin/'}
        x=json.dumps(x)
        return HttpResponse(x)    
    if len(district)==0:
        county_obj = CountyTb.objects.get(county_name=str(county))
        hospital_details = HealthCenters(hospital_name=str(hos_name),hospital_type=str(hostype),hospital_address=str(address),country_name=country_obj,county_name=county_obj,parent_hospital=str(parenthos),active=status)
        hospital_details.save()
        x = {"result":'/admin/'}
        x=json.dumps(x)
        return HttpResponse(x)
        # district_obj = Disttab.objects.get(district_name=str(district))
    if len(str(subdistrict)) ==0:
        # subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(subdistrict))
        county_obj = CountyTb.objects.get(county_name=str(county))
        district_obj = Disttab.objects.get(district_name=str(district))
        hospital_details = HealthCenters(hospital_name=str(hos_name),hospital_type=str(hostype),hospital_address=str(address),country_name=country_obj,county_name=county_obj,district_name=district_obj,parent_hospital=str(parenthos),active=status)
        hospital_details.save()
        x = {"result":'/admin/'}
        x=json.dumps(x)
        return HttpResponse(x)

    county_obj = CountyTb.objects.get(county_name=str(county))
    district_obj = Disttab.objects.get(district_name=str(district))
    subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(subdistrict))
    hospital_details = HealthCenters(hospital_name=str(hos_name),hospital_type=str(hostype),hospital_address=str(address),country_name=country_obj,county_name=county_obj,district_name=district_obj,subdistrict_name=subdistrict_obj,parent_hospital=str(parenthos),villages=str(villages),active=status)
    hospital_details.save()
    x = {"result":'/admin/'}
    x=json.dumps(x)
    return HttpResponse(x)

def update_hospitaldetail(request):

    global hosp_id
    if request.method == 'GET':
        hos_name = request.GET.get('name','')
        hostype = request.GET.get('type','')
        address = request.GET.get('add','')
        country = request.GET.get('hos_country','')
        county = request.GET.get('hos_county','')
        district =request.GET.get('hos_district','')
        subdistrict =request.GET.get('hos_subdistrict','')
        villages = request.GET.get('hos_village','')
        parenthos = request.GET.get('parent_hos','')
        active=request.GET.get('active','')

    elif request.method == 'POST':
        hos_name = request.POST.get('name','')
        hostype = request.POST.get('type','')
        address = request.POST.get('add','')
        country = request.POST.get('hos_country','')
        county = request.POST.get('hos_county','')
        district =request.POST.get('hos_district','')
        subdistrict =request.POST.get('hos_subdistrict','')
        villages = request.POST.get('hos_village','')
        parenthos = request.POST.get('parent_hos','')
        active=request.POST.get('active','')
    status = 0
    if str(active) == 'true':
        status = 1
    country_obj = CountryTb.objects.get(country_name=str(country))
    if str(county)=="null":
        edit_hospital = HealthCenters.objects.filter(id=hosp_id).update(hospital_name=str(hos_name),hospital_type=str(hostype),hospital_address=str(address),country_name=country_obj,parent_hospital=str(parenthos),active=status)
        x = {"result":'/admin/'}
        x=json.dumps(x)
        return HttpResponse(x)
    if str(district)=='null':
        county_obj = CountyTb.objects.get(county_name=str(county))
        edit_hospital = HealthCenters.objects.filter(id=hosp_id).update(hospital_name=str(hos_name),hospital_type=str(hostype),hospital_address=str(address),country_name=country_obj,county_name=county_obj,parent_hospital=str(parenthos),active=status)

        x = {"result":'/admin/'}
        x=json.dumps(x)
        return HttpResponse(x)
    if str(subdistrict) =='null':
        county_obj = CountyTb.objects.get(county_name=str(county))
        district_obj = Disttab.objects.get(district_name=str(district))
        edit_hospital = HealthCenters.objects.filter(id=hosp_id).update(hospital_name=str(hos_name),hospital_type=str(hostype),hospital_address=str(address),country_name=country_obj,county_name=county_obj,district_name=district_obj,parent_hospital=str(parenthos),active=status)
        x = {"result":'/admin/'}
        x=json.dumps(x)
        return HttpResponse(x)

    county_obj = CountyTb.objects.get(county_name=str(county))
    district_obj = Disttab.objects.get(district_name=str(district))
    subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(subdistrict))
    edit_hospital = HealthCenters.objects.filter(id=hosp_id).update(hospital_name=str(hos_name),hospital_type=str(hostype),hospital_address=str(address),country_name=country_obj,county_name=county_obj,district_name=district_obj,subdistrict_name=subdistrict_obj,parent_hospital=str(parenthos),villages=str(villages),active=status)

    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)

def hospital_validate(request):
    if request.method == "GET":
        hosp_id = int(request.GET.get("id",""))
        hosp_name = str(request.GET.get("hname",""))
    hosp_login = HealthCenters.objects.filter(hospital_name=hosp_name).values_list('id','hospital_name')
    login = "true"
    if len(hosp_login)>0 and hosp_id != hosp_login[0][0]:
        login = "false"
    return HttpResponse(login)

def data_list(current_values,all_data):
    data=[]
    data.insert(0,str(current_values))
    for name in all_data:
        if str(name[0]) not in data:
            data.append(str(name[0]))
    return data

def parent_hospital(current_hospital,list_of_hospitals):
    parent_hos=[]
    if str(current_hospital) == 'null':
        return parent_hos
    else:
        parent_hos.insert(0,current_hospital)
        for hospital in list_of_hospitals:
            hos_temp = hospital[0].strip()
            if hos_temp not in parent_hos:
                parent_hos.append(str(hos_temp))
        return parent_hos

def edit_hospital(request,hospital_id):
    global hosp_id
    hosp_id = hospital_id
    if request.method == 'GET':
        edit_details = HealthCenters.objects.get(id=int(hospital_id))
    elif request.method == 'POST':
        edit_details = HealthCenters.objects.get(id=int(hospital_id))

    hospital_types=['Country','County','District','SubDistrict','PHC','Subcenter']
    hostype = []
    hostype.insert(0,edit_details.hospital_type)
    for hos_types in hospital_types:
        if hos_types not in hostype:
            hostype.append(hos_types)
    parent_hos =[]
    status = edit_details.active
    c_status='false'
    if status == True:
        c_status = 'true'
    c = {}
    c.update(csrf(request))
    country_names= list(CountryTb.objects.filter(active=True).values_list('country_name'))
    e_country_name = CountryTb.objects.filter(id=int(edit_details.country_name.id)).values_list("country_name")[0][0]
    country = data_list(edit_details.country_name,country_names)

    if str(edit_details.hospital_type) == 'Country':
        return render_to_response('edithospital1.html',{'edit_details':edit_details,'country':country,'parenthos':parent_hos,'hostype':hostype,'active':c_status,'csrf_token':c['csrf_token']})

    elif str(edit_details.hospital_type) == 'County':
        parent_hos_names = HealthCenters.objects.filter(hospital_type='Country',country_name=int(edit_details.country_name.id),active=True).values_list('hospital_name')
        parent_hos = parent_hospital(edit_details.parent_hospital,parent_hos_names)
        county_name = CountyTb.objects.filter(country_name__country_name=str(edit_details.country_name),active=True).values_list('county_name')
        county = data_list(str(edit_details.county_name),county_name)
        return render_to_response('edithospital1.html',{'edit_details':edit_details,'country':country,'county':county,'hostype':hostype,'parenthos':parent_hos,'active':c_status,'csrf_token':c['csrf_token']})

    elif str(edit_details.hospital_type) == 'District':
        parent_hos_names = HealthCenters.objects.filter(hospital_type='County',county_name=int(edit_details.county_name.id),active=True).values_list('hospital_name')
        parent_hos = parent_hospital(edit_details.parent_hospital,parent_hos_names)
        county_name = CountyTb.objects.filter(country_name__country_name=str(edit_details.country_name),active=True).values_list('county_name')
        county = data_list(str(edit_details.county_name),county_name)
        district_names = Disttab.objects.filter(county_name=edit_details.county_name,active=True).values_list('district_name')
        district = data_list(edit_details.district_name,district_names)
        return render_to_response('edithospital1.html',{'edit_details':edit_details,'country':country,'county':county,'district':district,'hostype':hostype,'parenthos':parent_hos,'active':c_status,'csrf_token':c['csrf_token']})

    elif str(edit_details.hospital_type) == 'SubDistrict':
        parent_hos_names = HealthCenters.objects.filter(hospital_type='District',district_name=int(edit_details.district_name.id),active=True).values_list('hospital_name')
        parent_hos = parent_hospital(edit_details.parent_hospital,parent_hos_names)
        county_name = CountyTb.objects.filter(country_name__country_name=str(edit_details.country_name),active=True).values_list('county_name')
        county = data_list(str(edit_details.county_name),county_name)
        district_names = Disttab.objects.filter(county_name=edit_details.county_name,active=True).values_list('district_name')
        district = data_list(edit_details.district_name,district_names)
        subdistrict_names = SubdistrictTab.objects.filter(district=int(edit_details.district_name.id),active=True).values_list('subdistrict')
        subdistrict = data_list(edit_details.subdistrict_name,subdistrict_names)
        return render_to_response('edithospital1.html',{'edit_details':edit_details,'country':country,'county':county,'district':district,'subdistrict':subdistrict,'hostype':hostype,'parenthos':parent_hos,'active':c_status,'csrf_token':c['csrf_token']})

    elif str(edit_details.hospital_type) == 'PHC':
        parent_hos_names = HealthCenters.objects.filter(hospital_type='SubDistrict',subdistrict_name=int(edit_details.subdistrict_name.id),active=True).values_list('hospital_name')
        parent_hos = parent_hospital(edit_details.parent_hospital,parent_hos_names)
        county_name = CountyTb.objects.filter(country_name__country_name=str(edit_details.country_name),active=True).values_list('county_name')
        county = data_list(str(edit_details.county_name),county_name)
        district_names = Disttab.objects.filter(county_name=edit_details.county_name,active=True).values_list('district_name')
        district = data_list(edit_details.district_name,district_names)
        subdistrict_names = SubdistrictTab.objects.filter(district=int(edit_details.district_name.id),active=True).values_list('subdistrict')
        subdistrict = data_list(edit_details.subdistrict_name,subdistrict_names)
        return render_to_response('edithospital1.html',{'edit_details':edit_details,'country':country,'county':county,'district':district,'subdistrict':subdistrict,'hostype':hostype,'parenthos':parent_hos,'active':c_status,'csrf_token':c['csrf_token']})

    elif str(edit_details.hospital_type) == 'Subcenter':
        parent_hos_names = HealthCenters.objects.filter(hospital_type='PHC',subdistrict_name=int(edit_details.subdistrict_name.id),active=True).values_list('hospital_name')
        parent_hos = parent_hospital(edit_details.parent_hospital,parent_hos_names)
        county_name = CountyTb.objects.filter(country_name__country_name=str(edit_details.country_name),active=True).values_list('county_name')
        county = data_list(str(edit_details.county_name),county_name)
        district_names = Disttab.objects.filter(county_name=edit_details.county_name,active=True).values_list('district_name')
        district = data_list(edit_details.district_name,district_names)
        subdistrict_names = SubdistrictTab.objects.filter(district=int(edit_details.district_name.id),active=True).values_list('subdistrict')
        subdistrict = data_list(edit_details.subdistrict_name,subdistrict_names)
        location_name = LocationTab.objects.filter(subdistrict=int(edit_details.subdistrict_name.id),active=True).values_list('location')
        assigned_villages= edit_details.villages.split(",")
        remaining_villages = [village[0] for village in location_name if village[0] not in assigned_villages]
        return render_to_response('edithospital1.html',{'edit_details':edit_details,'country':country,'county':county,'district':district,'subdistrict':subdistrict,'hostype':hostype,'parenthos':parent_hos,'villages':assigned_villages,'rvillages':remaining_villages,'active':c_status,'csrf_token':c['csrf_token']})

def adminadd_usermaintenance(request):
    countryname = CountryTb.objects.filter(active=True).values_list('country_name')

    country_name=[]
    for n in countryname:
        country_name.append(n[0])
    c = {}
    c.update(csrf(request))
    return render_to_response('adduser.html',{'x':country_name,'csrf_token':c['csrf_token']})


def parenthos_detail(request):
    village=[]
    if request.method=='GET':
        p_country_name = str(request.GET.get('country',''))
        p_county_name = str(request.GET.get('county',''))
        p_district_name = str(request.GET.get('district',''))
        p_subdistrict_name = str(request.GET.get('subdistrict',''))
        # p_location = str(request.GET.get('location',''))
        p_hostype = str(request.GET.get('hos_type',''))
    country_obj = CountryTb.objects.get(country_name=str(p_country_name))
    if p_hostype == 'County':
        county_obj = CountyTb.objects.get(county_name=str(p_county_name))
        parent_hos_names = HealthCenters.objects.filter(hospital_type='Country',country_name=country_obj,active=True).values_list('hospital_name')
    elif p_hostype == 'District':
        county_obj = CountyTb.objects.get(county_name=str(p_county_name))
        district_obj = Disttab.objects.get(district_name=str(p_district_name))
        parent_hos_names = HealthCenters.objects.filter(hospital_type='County',county_name=county_obj,active=True).values_list('hospital_name')
    elif p_hostype == 'SubDistrict':
        county_obj = CountyTb.objects.get(county_name=str(p_county_name))
        district_obj = Disttab.objects.get(district_name=str(p_district_name))
        subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(p_subdistrict_name))
        parent_hos_names = HealthCenters.objects.filter(hospital_type='District',district_name=district_obj,active=True).values_list('hospital_name')
    elif p_hostype == 'PHC':
        county_obj = CountyTb.objects.get(county_name=str(p_county_name))
        district_obj = Disttab.objects.get(district_name=str(p_district_name))
        subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(p_subdistrict_name))
        parent_hos_names = HealthCenters.objects.filter(hospital_type='SubDistrict',subdistrict_name=subdistrict_obj,active=True).values_list('hospital_name')
    elif p_hostype == 'Subcenter':
        county_obj = CountyTb.objects.get(county_name=str(p_county_name))
        district_obj = Disttab.objects.get(district_name=str(p_district_name))
        subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(p_subdistrict_name))
        parent_hos_names = HealthCenters.objects.filter(hospital_type='PHC',subdistrict_name=subdistrict_obj,active=True).values_list('hospital_name')
        villages_data = LocationTab.objects.filter(subdistrict=subdistrict_obj,active=True).values_list('location')
        if len(villages_data) > 0:
            for v in villages_data:
                village.append(v[0])
    res = []
    for p in parent_hos_names:
        res.append(str(p[0]))

    result = {'res':res,'village':village}
    res = json.dumps(result)
    return HttpResponse(res)

def save_usermaintenance(request):
    if request.method == 'GET':
        userrole = request.GET.get('userrole','')
        userid = request.GET.get('userid','')
        first_name = request.GET.get('first_name','')
        last_name = request.GET.get('last_name','')
        password = request.GET.get('password','')
        mobile = request.GET.get('mobile','')
        email = request.GET.get('email','')
        countryname=request.GET.get('country_name','')
        countyname=request.GET.get('county_name','')
        districtname=request.GET.get('district_name','')
        subdistrictname=request.GET.get('subdistrict_name','')
        subcentername=request.GET.get('subcenter_name')
        village = request.GET.get('village','')
        hospital_name = request.GET.get('hospitals','')
        active = str(request.GET.get('active',''))

    elif request.method == 'POST':
        userrole = request.POST.get('userrole','')
        userid = request.POST.get('userid','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        password = request.POST.get('password','')
        mobile = request.POST.get('mobile','')
        email = request.POST.get('email','')
        village = request.POST.get('village','')
        countryname=request.POST.get('country_name','')
        countyname=request.POST.get('county_name','')
        districtname=request.POST.get('district_name','')
        subdistrictname=request.POST.get('subdistrict_name','')
        subcentername=request.POST.get('subcenter_name')
        hospital_name = request.POST.get('hospitals','')
        active = str(request.POST.get('active',''))

    pwd = hashlib.sha1()
    pwd.update(password)
    password = pwd.hexdigest()
    status=0
    if str(active) =='true':
        status=1
    country_obj = CountryTb.objects.get(country_name=str(countryname))

    if str(userrole) == 'ANM':
        county_obj = CountyTb.objects.get(county_name=str(countyname))
        district_obj = Disttab.objects.get(district_name=str(districtname))
        subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(subdistrictname))
        subcenter = HealthCenters.objects.get(hospital_name=str(subcentername))
        village_details = UserMasters(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),villages=str(village),phone_number=str(mobile),email=str(email),country=country_obj,county=county_obj,district=district_obj,subdistrict=subdistrict_obj,subcenter=subcenter,active=status,)
        village_details.save()

    elif str(userrole) == 'DOC':
        if len(countyname)==0:

            hospital_name=HealthCenters.objects.get(hospital_name=str(hospital_name))
            village_details = UserMasters(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),hospital=hospital_name,phone_number=str(mobile),email=str(email),country=country_obj,active=status)
            village_details.save()
            x = {"result":1}
            x=json.dumps(x)
            return HttpResponse(x)
        if len(districtname)==0:
            county_obj = CountyTb.objects.get(county_name=str(countyname))
            hospital_name=HealthCenters.objects.get(hospital_name=str(hospital_name))
            village_details = UserMasters(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),hospital=hospital_name,phone_number=str(mobile),email=str(email),country=country_obj,county=county_obj,active=status)
            village_details.save()
            x = {"result":1}
            x=json.dumps(x)
            return HttpResponse(x)
        if len(subdistrictname)==0:
            county_obj = CountyTb.objects.get(county_name=str(countyname))
            district_obj = Disttab.objects.get(district_name=str(districtname))
            hospital_name=HealthCenters.objects.get(hospital_name=str(hospital_name))
            village_details = UserMasters(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),hospital=hospital_name,phone_number=str(mobile),email=str(email),country=country_obj,county=county_obj,district=district_obj,active=status)
            village_details.save()
            x = {"result":1}
            x=json.dumps(x)
            return HttpResponse(x)

        county_obj = CountyTb.objects.get(county_name=str(countyname))
        district_obj = Disttab.objects.get(district_name=str(districtname))
        subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(subdistrictname))
        hospital_name= str(hospital_name).replace(" (PHC)","")
        hospital_name=HealthCenters.objects.get(hospital_name=str(hospital_name))
        village_details = UserMasters(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),hospital=hospital_name,phone_number=str(mobile),email=str(email),country=country_obj,county=county_obj,district=district_obj,subdistrict=subdistrict_obj,active=status)
        village_details.save()
    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)

# def subcenter_list(currentvalue,all_subcenters):
#     subcenter= []
#
#     subcenter.insert(0,currentvalue)
#     for s in all_subcenters:
#         if s[0] not in subcenter:
#             subcenter.append(s[0])
#     return subcenter

def edit_usermaintenance(request,batch_id):
    global user_id
    user_id = batch_id
    details=UserMasters.objects.get(id=int(batch_id))
    user_role = []
    if str(details.user_role) == 'ANM':
        user_role.insert(0,'ANM')
        user_role.append('DOC')
    elif str(details.user_role) == 'DOC':
        user_role.insert(0,details.user_role)
        user_role.append('ANM')
    country_names= list(CountryTb.objects.filter(active=True).values_list('country_name'))
    country = data_list(details.country,country_names)
    status= details.active
    c_status="false"
    if status == True:
        c_status = "true"
    c = {}
    c.update(csrf(request))
    
    if str(details.user_role) == 'ANM':
        county_name = CountyTb.objects.filter(country_name__country_name=str(details.country),active=True).values_list('county_name')
        county = data_list(str(details.county),county_name)
        district_names = Disttab.objects.filter(county_name=details.county,active=True).values_list('district_name')
        districts = data_list(details.district,district_names)
        subdistrict_names = SubdistrictTab.objects.filter(district__district_name=str(details.district),active=True).values_list('subdistrict')
        subdistricts = data_list(details.subdistrict,subdistrict_names)
        subcenter_data = HealthCenters.objects.filter(subdistrict_name__subdistrict=str(details.subdistrict),hospital_type='Subcenter',active=True).values_list('hospital_name')
        subcenters = data_list(details.subcenter,subcenter_data)
        assigned_villages= details.villages.split(",")
        village_data = HealthCenters.objects.filter(hospital_name=str(details.subcenter),hospital_type='Subcenter',active=True).values_list('villages')
        villages = details.villages.split(',')
        if len(village_data) > 0:
            village_data = village_data[0][0].split(",")
            villages = [village for village in village_data if village not in assigned_villages]
        return render_to_response('edituserdetail.html',{'y':details,'user_role':user_role,'country':country,'county':county,'district':districts,'subdistrict':subdistricts,'subcenter':subcenters,'villages':assigned_villages,"vil":villages,'active':c_status,'csrf_token':c['csrf_token']})
    
    elif str(details.user_role) == 'DOC':
        if str(details.county)=='None':
            hospital_name = HealthCenters.objects.filter(hospital_type='Country',country_name__country_name=str(details.country),active=True).values_list('hospital_name')
            hospital_list = data_list(details.hospital,hospital_name)
            return render_to_response('edituserdetail.html',{'y':details,'user_role':user_role,'country':country,'hospital':hospital_list,'active':c_status,'csrf_token':c['csrf_token']})

        if str(details.district) == 'None':
            county_name = CountyTb.objects.filter(country_name__country_name=str(details.country),active=True).values_list('county_name')
            county = data_list(str(details.county),county_name)
            hospital_name = HealthCenters.objects.filter(hospital_type='Country',country_name__country_name=str(details.country),active=True).values_list('hospital_name')
            hospital_list = data_list(details.hospital,hospital_name)
            return render_to_response('edituserdetail.html',{'y':details,'user_role':user_role,'country':country,'county':county,'hospital':hospital_list,'active':c_status,'csrf_token':c['csrf_token']})

        if str(details.subdistrict)=='None':
            county_name = CountyTb.objects.filter(country_name__country_name=str(details.country),active=True).values_list('county_name')
            county = data_list(str(details.county),county_name)
            hospital_name = HealthCenters.objects.filter(hospital_type='Country',country_name__country_name=str(details.country),active=True).values_list('hospital_name')
            hospital_list = data_list(details.hospital,hospital_name)
            district_names = Disttab.objects.filter(county_name=details.county,active=True).values_list('district_name')
            districts = data_list(details.district,district_names)
            return render_to_response('edituserdetail.html',{'y':details,'user_role':user_role,'country':country,'county':county,'district':districts,'hospital':hospital_list,'active':c_status,'csrf_token':c['csrf_token']})
        county_name = CountyTb.objects.filter(country_name__country_name=str(details.country),active=True).values_list('county_name')
        county = data_list(str(details.county),county_name)
        district_names = Disttab.objects.filter(county_name=details.county,active=True).values_list('district_name')
        districts = data_list(details.district,district_names)
        subdistrict_names = SubdistrictTab.objects.filter(district__district_name=str(details.district),active=True).values_list('subdistrict')
        subdistricts = data_list(details.subdistrict,subdistrict_names)
        phc_hospitals_name = HealthCenters.objects.filter(subdistrict_name=int(details.subdistrict.id),hospital_type='PHC',active=True).values_list('hospital_name')
        subd_hospitals_name = HealthCenters.objects.filter(subdistrict_name=int(details.subdistrict.id),hospital_type='SubDistrict',active=True).values_list('hospital_name')
        hospital_list=[]
        c_hospital_name = HealthCenters.objects.filter(id=int(details.hospital.id)).values_list('hospital_name')
        hospital_list.insert(0,c_hospital_name[0][0])
        for subd in subd_hospitals_name:
            if subd[0] not in hospital_list:
                hospital_list.append(subd[0])
        for phc in phc_hospitals_name:
            if str(phc[0]) not in hospital_list:
                hospital_list.append(str(phc[0]))
        return render_to_response('edituserdetail.html',{'y':details,'user_role':user_role,'country':country,'county':county,'district':districts,'subdistrict':subdistricts,'hospital':hospital_list,'active':c_status,'csrf_token':c['csrf_token']})

def user_validate(request):
    if request.method == "GET":
        user_id = int(request.GET.get("id",""))
        user_name = str(request.GET.get("uname",""))
    user_login = UserMasters.objects.filter(user_id=user_name).values_list('id','user_id')
    login = "true"
    if len(user_login)>0 and user_id != user_login[0][0]:
        login = "false"
    return HttpResponse(login)

def resetpassword(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('resetpassword.html',{'csrf_token':c['csrf_token']})

def save_password(request):
    if request.method == "GET":
        row_id = int(request.GET.get("id",""))
        password_name = request.GET.get("password","")
    user_data = UserMasters.objects.filter(id=row_id).values_list('user_id','user_role')
    if len(user_data) == 0:
        return HttpResponse('{"status":"Invalid user"}')
    user_id=str(user_data[0][0])
    user_role = settings.USER_ROLE[str(user_data[0][1])]
    pwd = hashlib.sha1()
    pwd.update(password_name)
    password = pwd.hexdigest()
    user_password = UserMasters.objects.filter(id=row_id).update(password=str(password))
    user_curl = "curl -s -H -X GET http://202.153.34.169:5984/drishti/_design/DrishtiUser/_view/by_username?key="+"%22"+str(user_id)+"%22"
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
    cmd = '''curl -s -H Content-Type:application/json -d '{"docs": [{"type": "DrishtiUser","username": "%s","password": "%s","active": true,"roles": ["%s"]  } ]}' -X POST http://202.153.34.169:5984/drishti/_bulk_docs''' %(str(user_id),str(password),str(user_role))
    res = commands.getstatusoutput(cmd)
    result={'res':"success"}
    x=json.dumps(result)
    return HttpResponse(x)

def update_usermaintenance(request):
    global user_id
    if request.method == 'GET':
        userrole = request.GET.get('userrole','')
        userid = request.GET.get('userid','')
        first_name = request.GET.get('first_name','')
        last_name = request.GET.get('last_name','')
        password = request.GET.get('password','')
        mobile = request.GET.get('mobile','')
        email = request.GET.get('email','')
        countryname=request.GET.get('country_name','')
        countyname=request.GET.get('county_name','')
        districtname=request.GET.get('district_name','')
        subdistrictname=request.GET.get('subdistrict_name','')
        subcentername=request.GET.get('subcenter_name','')
        village = request.GET.get('village','')
        hospital_name = request.GET.get('hospitals','')
        active = str(request.GET.get('active',''))


    elif request.method == 'POST':
        userrole = request.POST.get('userrole','')
        userid = request.POST.get('userid','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        password = request.POST.get('password','')
        mobile = request.POST.get('mobile','')
        email = request.POST.get('email','')
        village = request.POST.get('village','')
        countryname=request.POST.get('country_name','')
        countyname=request.POST.get('county_name','')
        districtname=request.POST.get('district_name','')
        subdistrictname=request.POST.get('subdistrict_name','')
        subcentername=request.POST.get('subcenter_name','')
        hospital_name = request.POST.get('hospitals','')
        active = str(request.POST.get('active',''))
    status=0
    if str(active) =='true':
        status=1
    country_obj = CountryTb.objects.get(country_name=str(countryname))
    if str(userrole) == 'ANM':
        county_obj = CountyTb.objects.get(county_name=str(countyname))
        district_obj = Disttab.objects.get(district_name=str(districtname))
        subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(subdistrictname))
        subcenter = HealthCenters.objects.get(hospital_name=str(subcentername))
        edit_details = UserMasters.objects.filter(id=user_id).update(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),subcenter=subcenter,phone_number=str(mobile),email=str(email),country=country_obj,county=county_obj,district=district_obj,subdistrict=subdistrict_obj,villages=str(village),active=status)

    elif str(userrole) == 'DOC':
        if len(countyname)==0:

            hospital_name=HealthCenters.objects.get(hospital_name=str(hospital_name))
            edit_details = UserMasters.objects.filter(id=user_id).update(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),hospital=hospital_name,phone_number=str(mobile),email=str(email),country=country_obj,active=status)

            x = {"result":1}
            x=json.dumps(x)
            return HttpResponse(x)
        if len(districtname)==0:
            county_obj = CountyTb.objects.get(county_name=str(countyname))
            hospital_name=HealthCenters.objects.get(hospital_name=str(hospital_name))
            edit_details = UserMasters.objects.filter(id=user_id).update(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),hospital=hospital_name,phone_number=str(mobile),email=str(email),country=country_obj,county=county_obj,active=status)

            x = {"result":1}
            x=json.dumps(x)
            return HttpResponse(x)
        if len(subdistrictname)==0:
            county_obj = CountyTb.objects.get(county_name=str(countyname))
            district_obj = Disttab.objects.get(district_name=str(districtname))
            hospital_name=HealthCenters.objects.get(hospital_name=str(hospital_name))
            edit_details = UserMasters.objects.filter(id=user_id).update(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),hospital=hospital_name,phone_number=str(mobile),email=str(email),country=country_obj,county=county_obj,district=district_obj,active=status)
            x = {"result":1}
            x=json.dumps(x)
            return HttpResponse(x)

        county_obj = CountyTb.objects.get(county_name=str(countyname))
        district_obj = Disttab.objects.get(district_name=str(districtname))
        subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(subdistrictname))
        hospital_name=HealthCenters.objects.get(hospital_name=str(hospital_name))
        
        edit_details = UserMasters.objects.filter(id=user_id).update(user_role=str(userrole),user_id=str(userid),name=str(first_name),lastname=str(last_name),password=str(password),hospital=hospital_name,phone_number=str(mobile),email=str(email),country=country_obj,county=county_obj,district=district_obj,subdistrict=subdistrict_obj,villages=str(village),active=status)
    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)

def county(request):
    if request.method == "GET":
        country_name= request.GET.get('country_name',"")

    elif request.method == "POST":
        country_name= request.POST.get('country_name',"")

    country_obj = CountryTb.objects.get(country_name=str(country_name))
    county_data = CountyTb.objects.filter(country_name=country_obj,active=True).values_list('county_name')
    hospitals_name = HealthCenters.objects.filter(country_name=country_obj,hospital_type='Country',active=True).values_list('hospital_name')
    hos_names =[]
    if len(hospitals_name)>0:
        for h in hospitals_name:
            hos_names.append(h[0])
    res = []
    for c in county_data:
        res.append(str(c[0]))
    result = {'res':res,'hospitals':hos_names}
    res = json.dumps(result)
    return HttpResponse(res)

def adminadd_district(request):
    countryname = CountryTb.objects.filter(active=True).values_list('country_name')

    country_name=[]
    for n in countryname:
        country_name.append(n[0])

    c = {}
    c.update(csrf(request))
    return render_to_response('adddistrict1.html',{'x':country_name,'csrf_token':c['csrf_token']})

def save_district(request):
    if request.method=="GET":
        country_name = request.GET.get("country","")
        county_name = request.GET.get("county","")
        district_name = request.GET.get("district","")
        active =request.GET.get("active","")
    status = 0
    if str(active) == 'true':
        status = 1
    country_obj = CountryTb.objects.get(country_name=str(country_name))
    county_obj = CountyTb.objects.get(county_name=str(county_name))
    ins_district= Disttab(country_name=country_obj,county_name=county_obj,district_name=str(district_name),active=status)
    ins_district.save()
    x = {"result":"true"}
    x=json.dumps(x)
    return HttpResponse(x)

def edit_district(request,district_id):
    global hos_id
    hos_id = district_id

    if request.method == 'GET':
        edit_details = Disttab.objects.get(id=int(district_id))
    elif request.method == 'POST':
        edit_details = Disttab.objects.get(id=int(district_id))

    country = []
    country_name = CountryTb.objects.filter(active=True).values_list('country_name')
    e_country_name = CountryTb.objects.filter(id=int(edit_details.country_name.id)).values_list("country_name")[0][0]
    country.insert(0,e_country_name)
    for name in country_name:
        if name[0] not in country:
            country.append(str(name[0]))

    county = []
    country_obj = CountryTb.objects.get(country_name=str(edit_details.country_name))
    county_name = CountyTb.objects.filter(country_name=country_obj,active=True).values_list('county_name')
    e_county_name = CountyTb.objects.filter(id=int(edit_details.county_name.id)).values_list("county_name")[0][0]
    county.insert(0,e_county_name)
    for name in county_name:
        if name[0] not in county:
            county.append(str(name[0]))

    status = edit_details.active
    c_status='false'
    if status == True:
        c_status = 'true'
    c = {}
    c.update(csrf(request))
    return render_to_response('editdistrict.html',{'country':country,'county':county,'district':edit_details.district_name,'active':c_status,'csrf_token':c['csrf_token']})

def update_district(request):
    global hos_id
    if request.method == 'GET':
        country = request.GET.get('country','')
        county = request.GET.get('county','')
        district = str(request.GET.get('district',''))
        active = request.GET.get('active','')
    status=0
    if str(active) == 'true':
        status = 1
    country_obj = CountryTb.objects.get(country_name=str(country))
    county_obj = CountyTb.objects.get(county_name=str(county))
    update_details = Disttab.objects.filter(id=hos_id).update(country_name=country_obj,county_name=county_obj,district_name=str(district),active=status)
    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)

def district_validate(request):
    if request.method == "GET":
        dist_id = int(request.GET.get("id",""))
        dist_name = str(request.GET.get("dname",""))
    distname = Disttab.objects.filter(district_name=dist_name).values_list('id','district_name')
    login = "true"
    if len(distname)>0 and dist_id != int(distname[0][0]):
        login = "false"
    return HttpResponse(login)


def district(request):

    if request.method == "GET":
        county_name= request.GET.get('county_name',"")

    elif request.method == "POST":
        county_name= request.POST.get('county_name',"")
    county_obj=CountyTb.objects.filter(county_name=str(county_name)).values_list("id")[0][0]
    district_data = Disttab.objects.filter(county_name=county_obj,active=True).values_list('district_name')
    hospitals_name = HealthCenters.objects.filter(county_name=county_obj,hospital_type='County',active=True).values_list('hospital_name')
    hos_names =[]
    if len(hospitals_name)>0:
        for h in hospitals_name:
            hos_names.append(h[0])

    res = []
    for d in district_data:
        res.append(str(d[0]))
    result = {'res':res,'hospitals':hos_names}
    res = json.dumps(result)
    return HttpResponse(res)

def adminadd_subdistrict(request):
    countryname = CountryTb.objects.filter(active=True).values_list('country_name')

    country_name=[]
    for n in countryname:
        country_name.append(n[0])

    c = {}
    c.update(csrf(request))
    return render_to_response('addsubdistrict.html',{'x':country_name,'csrf_token':c['csrf_token']})

def save_subdist(request):
    if request.method=="GET":
        country_name = request.GET.get("country","")
        county_name = request.GET.get("county","")
        district_name = request.GET.get("district","")
        subdistrict_name = request.GET.get("subdistrict","")
        active = request.GET.get("active","")
    elif request.method=="POST":
        country_name = request.POST.get("country","")
        county_name = request.POST.get("county","")
        district_name = request.POST.get("district","")
        subdistrict_name = request.POST.get("subdistrict","")
        active = request.POST.get("active","")
    status=0
    if str(active) =='true':
        status=1
    country_obj=CountryTb.objects.get(country_name=str(country_name))
    county_obj = CountyTb.objects.get(county_name=str(county_name))
    district_obj = Disttab.objects.get(district_name=str(district_name))
    ins_subdistrict= SubdistrictTab(country=country_obj,county=county_obj,district=district_obj,subdistrict=str(subdistrict_name),active=status)
    ins_subdistrict.save()
    x = {"result":'/admin/'}
    x=json.dumps(x)
    return HttpResponse(x)

def subdistrict(request):
    
    if request.method == "GET":
        district_name= request.GET.get('district_name',"")

    elif request.method == "POST":
        district_name= request.POST.get('district_name',"")
    district_obj=Disttab.objects.filter(district_name=str(district_name)).values_list("id")[0][0]
    subdistrict_data = SubdistrictTab.objects.filter(district=district_obj,active=True).values_list('subdistrict')
    hospitals_name = HealthCenters.objects.filter(district_name=district_obj,hospital_type='District',active=True).values_list('hospital_name')
    hos_names =[]
    if len(hospitals_name)>0:
        for h in hospitals_name:
            hos_names.append(h[0])
    res = []
    for s in subdistrict_data:
        res.append(str(s[0]))
    result = {'res':res,'hospitals':hos_names}
    res = json.dumps(result)
    return HttpResponse(res)

def subdistrict_validate(request):
    if request.method == "GET":
        subdist_id = int(request.GET.get("id",""))
        subdist_name = str(request.GET.get("sname",""))
    subdistname = SubdistrictTab.objects.filter(subdistrict=subdist_name,active=True).values_list('id','subdistrict')
    login = "true"
    if len(subdistname)>0 and subdist_id != subdistname[0][0]:
        login = "false"
    return HttpResponse(login)

def edit_subdistrict(request,subdistrict_id):
    global hos_id
    hos_id = subdistrict_id
    if request.method == 'GET':
        edit_details = SubdistrictTab.objects.get(id=int(subdistrict_id))
    elif request.method == 'POST':
        edit_details = SubdistrictTab.objects.get(id=int(subdistrict_id))

    country = []
    country_name = CountryTb.objects.filter(active=True).values_list('country_name')
    e_country_name = CountryTb.objects.filter(id=int(edit_details.country.id)).values_list("country_name")[0][0]
    country.insert(0,e_country_name)
    for name in country_name:
        if name[0] not in country:
            country.append(str(name[0]))

    county = []
    county_name = CountyTb.objects.filter(active=True).values_list('county_name')
    e_county_name = CountyTb.objects.filter(id=int(edit_details.county.id)).values_list("county_name")[0][0]
    county.insert(0,e_county_name)
    for name in county_name:
        if name[0] not in county:
            county.append(str(name[0]))

    district = []
    district_name = Disttab.objects.filter(active=True).values_list('district_name')
    e_district_name = Disttab.objects.filter(id = int(edit_details.district.id)).values_list("district_name")[0][0]
    district.insert(0,e_district_name)
    for name in district_name:
        if name[0] not in district:
            district.append(str(name[0]))
    status = edit_details.active
    c_status='false'
    if status == True:
        c_status = 'true'
    c = {}
    c.update(csrf(request))
    return render_to_response('editsubdistrict.html',{'country':country,'county':county,'district':district,'subdistrict':edit_details.subdistrict,'active':c_status,'csrf_token':c['csrf_token']})

def update_subdistrict(request):
    global hos_id
    if request.method == 'GET':
        country = str(request.GET.get('country',''))
        county = str(request.GET.get('county',''))
        district = str(request.GET.get('district',''))
        subdistrict = str(request.GET.get('subdistrict',''))
        active = str(request.GET.get('active',''))
    status=0
    if str(active) =='true':
        status=1
    country_obj = CountryTb.objects.get(country_name=country)
    county_obj = CountyTb.objects.get(county_name=county)
    district_obj = Disttab.objects.get(district_name =district)
    update_details = SubdistrictTab.objects.filter(id=hos_id).update(country=country_obj,county=county_obj,district=district_obj,subdistrict=subdistrict,active=status)

    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)

def adminadd_location(request):
    countryname = CountryTb.objects.filter(active=True).values_list('country_name')
    country_name=[]
    for n in countryname:
        country_name.append(n[0])

    c = {}
    c.update(csrf(request))
    return render_to_response('addlocation.html',{'x':country_name,'csrf_token':c['csrf_token']})

def save_location(request):
    if request.method=="GET":
        country_name = request.GET.get("country","")
        county_name = request.GET.get("county","")
        district_name = request.GET.get("district","")
        subdistrict_name = request.GET.get("subdistrict","")
        location_name = request.GET.get("location","")
        active = str(request.GET.get('active',''))
    status=0
    if str(active) =='true':
        status=1
    country_obj=CountryTb.objects.get(country_name=str(country_name))
    county_obj = CountyTb.objects.get(county_name=str(county_name))
    district_obj = Disttab.objects.get(district_name=str(district_name))
    subdistrict_obj = SubdistrictTab.objects.get(subdistrict=str(subdistrict_name))
    ins_location= LocationTab(country=country_obj,county=county_obj,district=district_obj,subdistrict=subdistrict_obj,location=str(location_name),active=status)
    save_res=ins_location.save()
    messages = {"messages":'/admin/'}
    messages=json.dumps(messages)
    return HttpResponse(messages)

def edit_location(request,loc_id):
    global hos_id
    hos_id = loc_id
    if request.method == 'GET':
        edit_details = LocationTab.objects.get(id=int(loc_id))
    elif request.method == 'POST':
        edit_details = LocationTab.objects.get(id=int(loc_id))

    country = []
    country_name = CountryTb.objects.filter(active=True).values_list('country_name')
    e_country_name = CountryTb.objects.filter(id=int(edit_details.country.id)).values_list("country_name")[0][0]
    country.insert(0,e_country_name)
    for name in country_name:
        if name[0] not in country:
            country.append(str(name[0]))
    county = []
    county_name = CountyTb.objects.filter(active=True).values_list('county_name')
    e_county_name = CountyTb.objects.filter(id=int(edit_details.county.id)).values_list("county_name")[0][0]
    county.insert(0,e_county_name)
    for name in county_name:
        if name[0] not in county:
            county.append(str(name[0]))

    district = []
    district_name = Disttab.objects.filter(active=True).values_list('district_name')
    e_district_name = Disttab.objects.filter(id=int(edit_details.district.id)).values_list("district_name")[0][0]
    district.insert(0,e_district_name)
    for name in district_name:
        if name[0] not in district:
            district.append(str(name[0]))
    subdistrict = []
    subdistrict_name = SubdistrictTab.objects.filter(active=True).values_list('subdistrict')
    e_subdistrict_name = SubdistrictTab.objects.filter(id=int(edit_details.subdistrict.id)).values_list("subdistrict")[0][0]
    subdistrict.insert(0,e_subdistrict_name)
    for name in subdistrict_name:
        if name[0] not in subdistrict:
            subdistrict.append(str(name[0]))
    status= edit_details.active
    c_status='false'
    if status == True:
        c_status = 'true'
    c = {}
    c.update(csrf(request))
    return render_to_response('editlocation.html',{'country':country,'county':county,'district':district,'subdistrict':subdistrict,'location':edit_details.location,'active':c_status,'csrf_token':c['csrf_token']})

def update_location(request):
    global hos_id
    if request.method == 'GET':
        country = str(request.GET.get('country',''))
        county = str(request.GET.get('county',''))
        district = str(request.GET.get('district',''))
        subdistrict = str(request.GET.get('subdistrict',''))
        location = str(request.GET.get('location',''))
        active = str(request.GET.get('active',''))
    status=0
    if str(active) =='true':
        status=1
    previous_location = str(LocationTab.objects.filter(id=hos_id).values_list("location")[0][0])
    country_obj = CountryTb.objects.get(country_name=country)
    county_obj = CountyTb.objects.get(county_name =county)
    district_obj = Disttab.objects.get(district_name =district)
    subdistrict_obj = SubdistrictTab.objects.get(subdistrict=subdistrict)
    update_details = LocationTab.objects.filter(id=hos_id).update(country=country_obj,county=county_obj,district=district_obj,subdistrict=subdistrict_obj,location=str(location),active=status)
    cur = connection.cursor()
    health_centers_query = "update health_centers set villages=REPLACE(villages,'%s','%s')" %(previous_location,location)
    cur.execute(str(health_centers_query))
    user_masters_query = "update user_masters_new set villages=REPLACE(villages,'%s','%s')" %(previous_location,location)
    cur.execute(str(user_masters_query))
    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)

def location(request):
    if request.method == "GET":
        subdistrict_name= request.GET.get('subdistrict_name',"")

    elif request.method == "POST":
        subdistrict_name= request.POST.get('subdistrict_name',"")
    subdistrict_obj=SubdistrictTab.objects.filter(subdistrict=str(subdistrict_name))
    subdistrict_data = HealthCenters.objects.filter(subdistrict_name=subdistrict_obj,hospital_type='SubDistrict',active=True).values_list('hospital_name')
    location_data = LocationTab.objects.filter(subdistrict=subdistrict_obj,active=True).values_list('location')
    hospitals_name = HealthCenters.objects.filter(subdistrict_name=subdistrict_obj,hospital_type='PHC',active=True).values_list('hospital_name')
    subcenter_data = HealthCenters.objects.filter(subdistrict_name=subdistrict_obj,hospital_type='Subcenter',active=True).values_list('hospital_name')
    hos_names =[]
    if len(hospitals_name)>0:
        for h in hospitals_name:
            hos_names.append(h[0]+' (PHC)')
    res = []
    subcenter_list = []
    village=[]
    location = []
    for s in subdistrict_data:
        res.append(str(s[0]))
    for subcenter in subcenter_data:
        subcenter_list.append(str(subcenter[0]))
    for l in location_data:
        location.append(str(l[0]))
        village.append(str(l[0]))
    hos_names = res+hos_names
    result = {'res':res,'village':village,'hospitals':hos_names,'loc':location,"subcenter":subcenter_list}
    res = json.dumps(result)
    return HttpResponse(res)

def location_validate(request):
    if request.method == "GET":
        loc_id = int(request.GET.get("id",""))
        loc_name = str(request.GET.get("lname",""))
        country_name = str(request.GET.get("country_name",""))
    country_id = CountryTb.objects.filter(country_name=country_name).values_list('id')[0][0]
    locname = LocationTab.objects.filter(country=int(country_id),location=loc_name).values_list('id','location')
    login = "true"
    if len(locname)>0 and loc_id != locname[0][0]:
        login = "false"
    return HttpResponse(login)

def subcenter(request):
    if request.method == "GET":
        location_name= request.GET.get('location',"")

    elif request.method == "POST":
        location_name= request.POST.get('location',"")
    subcenter_data = HealthCenters.objects.filter(hospital_name=str(location_name),hospital_type='Subcenter',active=True).values_list('villages')
    if len(subcenter_data)==0:
        return HttpResponse('{"status":"Invalid location"}')
    res=[]
    if len(subcenter_data[0][0]) != 'null':
        res = subcenter_data[0][0].split(',')
    result = {'res':res}
    res = json.dumps(result)
    return HttpResponse(res)

def docoverview(request):
    if request.method == "GET":
        o_visitid = request.GET.get("visitid","")
        o_entityid =request.GET.get("entityid","")
    display_result=[]
    overview_data = []

    overview_visit_curl = ancvisit_detail="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_EntityId?key=%22"+str(o_visitid)+"%22&descending=true"
    overview_visit_output = commands.getoutput(overview_visit_curl)
    overview_visit_details = json.loads(overview_visit_output)
    overview_visit_data = overview_visit_details["rows"]
    for event in overview_visit_data:
        overview_events = {}
        if str(event['value'][0]) == 'pnc_visit' or str(event['value'][0]) == 'pnc_visit_edit':
            pnc_tags = ["pncNumber","pncVisitDate","difficulties1","difficulties2","abdominalProblems","urineStoolProblems",
                        "hasFeverSymptoms","breastProblems","vaginalProblems","bpSystolic","bpDiastolic","temperature","pulseRate",
                        "bloodGlucoseData","weight","anmPoc","pncVisitPlace","pncVisitDate","isHighRisk","hbLevel","docPocInfo"]
            f = lambda x: x[0].get("value") if len(x)>0 else ""

            fetched_dict = copyf(event["value"][1]["form"]["fields"],"name",pnc_tags)

            overview_events["pncNumber"]=f(copyf(fetched_dict,"name","pncNumber"))
            overview_events["visitDate"]=f(copyf(fetched_dict,"name","pncVisitDate"))
            difficulty1=str(f(copyf(fetched_dict,"name","difficulties1")))
            difficulty2=str(f(copyf(fetched_dict,"name","difficulties2")))
            abdominal_problem=str(f(copyf(fetched_dict,"name","abdominalProblems")))
            urineStoolProblems=str(f(copyf(fetched_dict,"name","urineStoolProblems")))
            hasFeverSymptoms=str(f(copyf(fetched_dict,"name","hasFeverSymptoms")))
            breastProblems=str(f(copyf(fetched_dict,"name","breastProblems")))
            vaginalProblems=str(f(copyf(fetched_dict,"name","vaginalProblems")))
            overview_events["riskObserved"]=difficulty1+","+difficulty2+","+abdominal_problem+","+urineStoolProblems+","+hasFeverSymptoms+","+breastProblems+","+vaginalProblems
            overview_events["bpSystolic"]=str(f(copyf(fetched_dict,"name","bpSystolic")))
            overview_events["bpDiastolic"]=f(copyf(fetched_dict,"name","bpDiastolic"))
            overview_events["temperature"]=f(copyf(fetched_dict,"name","temperature"))
            overview_events["pulseRate"]=str(f(copyf(fetched_dict,"name","pulseRate")))
            overview_events["bloodGlucoseData"]=f(copyf(fetched_dict,"name","bloodGlucoseData"))
            overview_events["weight"]=f(copyf(fetched_dict,"name","weight"))
            overview_events["anmPoc"]=f(copyf(fetched_dict,"name","anmPoc"))
            overview_events["visitPlace"]=f(copyf(fetched_dict,"name","visitPlace"))
            overview_events["visitDate"]=f(copyf(fetched_dict,"name","visitDate"))
            overview_events["isHighRisk"]=f(copyf(fetched_dict,"name","isHighRisk"))
            overview_events["hbLevel"]=f(copyf(fetched_dict,"name","hbLevel"))
            overview_events["docPocInfo"]=f(copyf(fetched_dict,"name","docPocInfo"))
            overview_events['visit_type'] = 'PNC'
            overview_events['server_version'] = event["value"][-1]
            overview_events['id'] = event["id"]
            overview_data.append(overview_events)
        elif str(event['value'][0]) == 'anc_visit' or str(event['value'][0]) == 'anc_visit_edit':
            anc_tags = ["ancVisitNumber","ancNumber","ancVisitPerson","ancVisitDate","riskObservedDuringANC","bpSystolic","bpDiastolic",
                        "temperature","pulseRate","bloodGlucoseData","weight","anmPoc","isHighRisk","fetalData","docPocInfo"]
            f = lambda x: x[0].get("value") if len(x)>0 else ""
            fetched_dict = copyf(event["value"][1]["form"]["fields"],"name",anc_tags)
            overview_events["visitNumber"]=f(copyf(fetched_dict,"name","ancVisitNumber"))
            overview_events["ancNumber"]=f(copyf(fetched_dict,"name","ancNumber"))
            overview_events["visitPerson"]=f(copyf(fetched_dict,"name","ancVisitPerson"))
            overview_events["visitDate"]=f(copyf(fetched_dict,"name","ancVisitDate"))
            overview_events["riskObserved"]=f(copyf(fetched_dict,"name","riskObservedDuringANC"))
            overview_events["bpSystolic"]=f(copyf(fetched_dict,"name","bpSystolic"))
            overview_events["bpDiastolic"]=f(copyf(fetched_dict,"name","bpDiastolic"))
            overview_events["temperature"]=f(copyf(fetched_dict,"name","temperature"))
            overview_events["pulseRate"]=str(f(copyf(fetched_dict,"name","pulseRate")))
            overview_events["bloodGlucoseData"]=f(copyf(fetched_dict,"name","bloodGlucoseData"))
            overview_events["weight"]=f(copyf(fetched_dict,"name","weight"))
            overview_events["anmPoc"]=f(copyf(fetched_dict,"name","anmPoc"))
            overview_events["isHighRisk"]=f(copyf(fetched_dict,"name","isHighRisk"))
            overview_events["fetalData"]=f(copyf(fetched_dict,"name","fetalData"))
            overview_events["docPocInfo"]=f(copyf(fetched_dict,"name","docPocInfo"))
            overview_events['visit_type'] = 'ANC'
            overview_events['server_version'] = event["value"][-1]
            overview_events['id'] = event["id"]
            overview_data.append(overview_events)
        elif str(event['value'][0]) == 'child_illness' or str(event['value'][0]) == 'child_illness_edit':

            child_tags = ["dateOfBirth","childSigns","childSignsOther","immediateReferral","immediateReferralReason","reportChildDisease","reportChildDiseaseOther",
                        "reportChildDiseaseDate","reportChildDiseasePlace","numberOfORSGiven","childReferral","anmPoc","isHighRisk","submissionDate","id","docPocInfo"]
            f = lambda x: x[0].get("value") if len(x)>0 else ""
            fetched_dict = copyf(event["value"][1]["form"]["fields"],"name",child_tags)
            overview_events["dateOfBirth"]=f(copyf(fetched_dict,"name","dateOfBirth"))
            overview_events["childSigns"]=f(copyf(fetched_dict,"name","childSigns"))
            overview_events["childSignsOther"]=f(copyf(fetched_dict,"name","childSignsOther"))
            overview_events["immediateReferral"]=f(copyf(fetched_dict,"name","immediateReferral"))
            overview_events["immediateReferralReason"]=f(copyf(fetched_dict,"name","immediateReferralReason"))
            overview_events["reportChildDisease"]=f(copyf(fetched_dict,"name","reportChildDisease"))
            overview_events["reportChildDiseaseOther"]=f(copyf(fetched_dict,"name","reportChildDiseaseOther"))
            overview_events["reportChildDiseaseDate"]=f(copyf(fetched_dict,"name","reportChildDiseaseDate"))
            overview_events["reportChildDiseasePlace"]=f(copyf(fetched_dict,"name","reportChildDiseasePlace"))
            overview_events["numberOfORSGiven"]=f(copyf(fetched_dict,"name","numberOfORSGiven"))
            overview_events["childReferral"]=f(copyf(fetched_dict,"name","childReferral"))
            overview_events["anmPoc"]=f(copyf(fetched_dict,"name","anmPoc"))
            overview_events["isHighRisk"]=f(copyf(fetched_dict,"name","isHighRisk"))
            overview_events["visitDate"]=f(copyf(fetched_dict,"name","submissionDate"))
            overview_events["docPocInfo"]=f(copyf(fetched_dict,"name","docPocInfo"))
            overview_events['visit_type'] = 'CHILD'
            overview_events['server_version'] = event["value"][-1]
            overview_events['id'] = event["id"]
            overview_data.append(overview_events)
    end_res= json.dumps(overview_data)
    return HttpResponse(end_res)
