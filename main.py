# Import time module
import time
 
# record start time
start = time.time()
import pymongo as py
import csv
import uuid
import datetime
from age_compo import add_age_to_compo
from vital_status_compo import vital_status
from risk_factors import save_risk_factors
from problem_list import save_problem_list
from laboratory_tests import save_laboratory_test_results
from demographics import add_demographic_data
#------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#Consents collection:
consents_coll=myclient["Consents"]["Consents Collection"]
#---------------------------------------------------------------------------------------
csv_file_path="heart_failure_clinical_records_dataset.csv"

def process_boolean(value):
    return value == '1'

def male_female(gender):
    if gender=='1':
        return "MALE"
    else:
        return "FEMALE"

with open(csv_file_path, 'r', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for idx, row in enumerate(csv_reader, start=1):
        if idx<3000:
            break
        #uuid generation for each user:
        uuid_= str(uuid.uuid4())

        #generating a virtual phone number for each patient
        phone_number= "+"+str(idx)

        #data extraction:
        age= round(float(row['age']))
        anaemia= process_boolean(row['anaemia'])
        creatinine_phosphokinase= float(row['creatinine_phosphokinase'])
        diabetes= process_boolean(row['diabetes'])
        ejection_fraction= float(row['ejection_fraction'])
        high_blood_pressure= process_boolean(row['high_blood_pressure'])
        platelets= float(row['platelets'])
        serum_creatinine= float(row['serum_creatinine'])
        serum_sodium= float(row['serum_sodium'])
        gender= male_female(row['sex'])
        smoking= process_boolean(row['smoking'])
        vital_status_= process_boolean(row['DEATH_EVENT'])

        problem_dict={
            'anaemia':anaemia,
            'diabetes':diabetes,
        }

        risk_factors_dict={
            'high_blood_pressure':high_blood_pressure,
            'smoking':smoking,
        }

        analyses_dict={
            'creatinine_phosphokinase':creatinine_phosphokinase,
            'ejection_fraction':ejection_fraction,
            'platelets':platelets,
            'serum_creatinine':serum_creatinine,
            'serum_sodium':serum_sodium,
        }

        #Giving anonymised values for resting demographic datapoints
        name,surname,country_of_birth,province_birth,town_birth,street_name,street_number,country,province,town="Patient",str(idx),"test","test","test","test",idx,"test","test","test"
        birthday="xxxx-xx-xx"
        dni="00000000X"
        postal_code="00000"
        current_date=str(datetime.date.today())
        
        json_object_demographic_data= add_demographic_data(name,surname,dni,gender,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,country,province,town)
        demographic_doc={
                    "uuid": uuid_,
                    "phone number": phone_number,
                    "current date": current_date,
                    "demographic data": json_object_demographic_data
                }
        demographic_data_coll.insert_one(demographic_doc)

        medical_data_dict={
            "uuid": uuid_,
            "saving date": current_date,
            "problem list": save_problem_list(problem_dict),
            "risk factors": save_risk_factors(risk_factors_dict),
            "vital status": vital_status(vital_status_),
            "age":add_age_to_compo(age),
        }

        medical_history_dict={
            "uuid": uuid_,
            "saving date": current_date,
            "analytics": [save_laboratory_test_results(analyses_dict),],
        }

        medical_data_coll.insert_one(medical_data_dict)
        medical_hist_coll.insert_one(medical_history_dict)

        existing_doc = consents_coll.find_one({"uuid":uuid_})
        if existing_doc is None:
            consents_coll.insert_one({"uuid":uuid_})


# record end time
end = time.time()

# print the difference between start
# and end time in milli. secs
print("The time of execution of above program is :",
    (end-start) * 10**3, "ms")