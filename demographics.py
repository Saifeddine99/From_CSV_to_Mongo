import json
#This function adds the submitted demographic_data to the demographics json file 
def add_demographic_data(name,surname,dni,gender,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,country,province,town):
    full_path_demographic_data = 'patient.v0_20230713112750_000001_1.json'
    #Demographic data file:
    with open(full_path_demographic_data, 'r') as openfile:
        # Reading from json file
        json_object_demographic_data = json.load(openfile)
    #Birth data:
    json_object_demographic_data["details"]["items"][0]["items"][0]["value"]["value"]=birthday
    json_object_demographic_data["details"]["items"][0]["items"][1]["value"]["value"]=country_of_birth
    json_object_demographic_data["details"]["items"][0]["items"][2]["value"]["value"]=province_birth
    json_object_demographic_data["details"]["items"][0]["items"][3]["value"]["value"]=town_birth
    json_object_demographic_data["details"]["items"][0]["items"][4]["value"]["value"]=gender
    json_object_demographic_data["details"]["items"][0]["items"][5]["value"]["value"]=dni

    #Other data:
    json_object_demographic_data["details"]["items"][3]["value"]["value"]=gender

    #Address:
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][0]["items"][0]["value"]["value"]=street_name
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][0]["items"][1]["value"]["value"]=street_number
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][1]["value"]["value"]=postal_code
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][2]["value"]["value"]=town
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][3]["value"]["value"]=province
    json_object_demographic_data["contacts"][0]["addresses"][0]["details"]["items"][4]["value"]["value"]=country

    #Identity:
    json_object_demographic_data["identities"][0]["details"]["items"][0]["value"]["value"]=name
    json_object_demographic_data["identities"][0]["details"]["items"][1]["value"]["value"]=surname

    return(json_object_demographic_data)