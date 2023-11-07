import json
import copy
def save_problem_list(problem_dict):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_problem_list_json = 'problem_list.v1_20230913120942_000001_1.json'
    #Demographic data file:
    with open(full_path_problem_list_json, 'r') as openfile:
        # Reading from json file
        json_object_problem_list = json.load(openfile)

    problem_list_=[]
    for problem,value in problem_dict.items():
        if value==True:
            problem_list_.append(copy.deepcopy(json_object_problem_list))
            problem_list_[-1]["content"][0]["items"][0]["data"]["items"][0]["value"]["value"] = problem.upper()

    return problem_list_