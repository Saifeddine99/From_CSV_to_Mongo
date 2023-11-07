import json
import copy
#---------------------------------------------------------------------------------------
def save_risk_factors(risk_factors_dict):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_risk_factors_json = 'risk_factors_20231002120317_000001_1.json'
    #Demographic data file:
    with open(full_path_risk_factors_json, 'r') as openfile:
        # Reading from json file
        json_object_risk_factors = json.load(openfile)

    risk_factors=[]
    for cvrf,value in risk_factors_dict.items():
        if(value):
            risk_factors.append(copy.deepcopy(json_object_risk_factors))
            risk_factors[-1]["content"][0]["data"]["items"][1]["items"][0]["value"]["value"] = cvrf.upper()
    
    return(risk_factors)