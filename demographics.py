import json
from encrypt import encrypt_data

#This function adds the submitted demographic_data to the demographics json file 
def add_demographic_data(name,surname,dni,gender,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,country,province,town):
    full_path_demographic_data = 'patient.v0_20230713112750_000001_1.json'
    #Demographic data file:
    with open(full_path_demographic_data, 'r') as openfile:
        # Reading from json file
        json_object_demographic_data = json.load(openfile)
    #Birth data:
    json_object_demographic_data["details"]["items"][0]["items"][0]["value"]["value"]=encrypt_data(birthday.upper())
    json_object_demographic_data["details"]["items"][0]["items"][1]["value"]["value"]=encrypt_data(country_of_birth.upper())
    json_object_demographic_data["details"]["items"][0]["items"][2]["value"]["value"]=encrypt_data(province_birth.upper())
    json_object_demographic_data["details"]["items"][0]["items"][3]["value"]["value"]=encrypt_data(town_birth.upper())
    json_object_demographic_data["details"]["items"][0]["items"][4]["value"]["value"]=encrypt_data(gender.upper())
    json_object_demographic_data["details"]["items"][0]["items"][5]["value"]["value"]=encrypt_data(dni.upper())

    #Other data:
    json_object_demographic_data["details"]["items"][3]["value"]["value"]=encrypt_data(gender.upper())

    #Address:
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][0]["items"][0]["value"]["value"]=encrypt_data(street_name.upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][0]["items"][1]["value"]["value"]=encrypt_data(str(street_number).upper())##########
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][1]["value"]["value"]=encrypt_data(postal_code.upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][2]["value"]["value"]=encrypt_data(town.upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][3]["value"]["value"]=encrypt_data(province.upper())
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][4]["value"]["value"]=encrypt_data(country.upper())

    #Identity:
    json_object_demographic_data["identities"][0]["details"]["items"][0]["value"]["value"]=encrypt_data(name.upper())
    json_object_demographic_data["identities"][0]["details"]["items"][1]["value"]["value"]=encrypt_data(surname.upper())

    return(json_object_demographic_data)