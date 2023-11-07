import json
def vital_status(vital_status):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_vital_status = 'vital_status_20231017124216_000001_1.json'
    #Demographic data file:
    with open(full_path_vital_status, 'r') as openfile:
        # Reading from json file
        json_object_vital_status= json.load(openfile)

    status="Unknown"
    code_string="at0009"

    if vital_status==True:
        status="Dead"
        code_string="at0006"
    elif vital_status==False:
        status="Alive"
        code_string="at0005"

    json_object_vital_status["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]=status
    json_object_vital_status["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["defining_code"]["code_string"]=code_string

    return(json_object_vital_status)