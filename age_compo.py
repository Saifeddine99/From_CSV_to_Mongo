import json
from encrypt import encrypt_data
def add_age_to_compo(age):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_age_compo = 'age.v1_20231106112026_000001_1.json'
    #Demographic data file:
    with open(full_path_age_compo, 'r') as openfile:
        # Reading from json file
        json_object_age_compo = json.load(openfile)

    json_object_age_compo["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]=encrypt_data(str(age))

    return(json_object_age_compo)