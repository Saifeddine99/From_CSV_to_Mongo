import json
import copy
from encrypt import encrypt_data

def save_laboratory_test_results(analyses_dict):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_laboratory_test_results = 'laboratory_result_report_20231003110928_000001_1.json'
    #Demographic data file:
    with open(full_path_laboratory_test_results, 'r') as openfile:
        # Reading from json file
        json_object_laboratory_test_results = json.load(openfile)

    laboratory_test_results_list=[]
    for test_name,test_result in analyses_dict.items():
        #Here we're generating deepcopies of "json_object_laboratory_test_results" to avoid modification of the previous copies.
        laboratory_test_results_list.append(copy.deepcopy(json_object_laboratory_test_results))
        laboratory_test_results_list[-1]["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]=encrypt_data(str(test_result))
        laboratory_test_results_list[-1]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]=encrypt_data(test_name.upper())
        
    return(laboratory_test_results_list)