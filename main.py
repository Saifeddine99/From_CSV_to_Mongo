# IF you want to remove all these records from databases run the clearing_databases.py script
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
from encrypt import encrypt_data
#------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#---------------------------------------------------------------------------------------
#This line saves the csv file path to the "csv_file_path" variable
csv_file_path="heart_failure_clinical_records_dataset.csv"

#This function returns "True" if value=='1' else it returns "False"
def process_boolean(value):
    return value == '1'

#This function returns "MALE" value if gender==1 and "FEMALE" value if gender==0
def male_female(gender):
    if gender=='1':
        return "MALE"
    else:
        return "FEMALE"

with open(csv_file_path, 'r', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for idx, row in enumerate(csv_reader, start=1):
        #To avoid multiple saving of the same records we made this simple condition. So, before saving change the condition to idx>3000
        if idx<3000:
            break
        #uuid generation for each user:
        uuid_= str(uuid.uuid4())

        #generating a virtual phone number for each patient
        phone_number= "+"+str(idx)

        # Data extraction:
        #assigning each value to its correspending variable:
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

        # "problem_dict" is a dictionary containing the list of medical diseases existing in the csv file.
        problem_dict={
            'anaemia':anaemia,
            'diabetes':diabetes,
        }
        # "risk_factors_dict" is a dictionary containing the list of risk factors existing in the csv file.
        risk_factors_dict={
            'high_blood_pressure':high_blood_pressure,
            'smoking':smoking,
        }
        # "analyses_dict" is a dictionary containing the list of all analysis + their results existing in the csv file.
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
        #"add_demographic_data" is a function allowing to save the demographic data following the OpenEHR format. 
        json_object_demographic_data= add_demographic_data(name,surname,dni,gender,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,country,province,town)
        #This will be the structure of the document to be saved in the demographic db.
        demographic_doc={
                    "uuid": uuid_,
                    "phone number": encrypt_data(phone_number),
                    "current date": encrypt_data(current_date),
                    "demographic data": json_object_demographic_data
                }
        demographic_data_coll.insert_one(demographic_doc)
        #This will be the structure of the document to be saved in the medical data db.
        medical_data_dict={
            "uuid": uuid_,
            "saving date": encrypt_data(current_date),
            "problem list": save_problem_list(problem_dict),
            "risk factors": save_risk_factors(risk_factors_dict),
            "vital status": vital_status(vital_status_),
            "age":add_age_to_compo(age),
        }
        #This will be the structure of the document to be saved in the medical history db.
        medical_history_dict={
            "uuid": uuid_,
            "saving date": encrypt_data(current_date),
            "analytics": [save_laboratory_test_results(analyses_dict),],
        }

        medical_data_coll.insert_one(medical_data_dict)
        medical_hist_coll.insert_one(medical_history_dict)

#Here we're calculating the total time this script takes to save all records to db.
# record end time
end = time.time()

# print the difference between start and end time in milli. secs
print("The time of execution of above program is :",
    (end-start) * 10**3, "ms")