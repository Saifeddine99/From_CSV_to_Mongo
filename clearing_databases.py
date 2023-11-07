from paths import parameter_to_directory
import pymongo as py
#---------------------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#---------------------------------------------------------------------------------------
cursor= demographic_data_coll.find({parameter_to_directory("Name"): {'$regex':  f'^{"Patient"}$', '$options': 'i'}})

uuid_list=[]
for demog_doc in cursor:
    uuid_list.append(demog_doc["uuid"])

medical_data_coll.delete_many({"uuid": {"$in":uuid_list}})
medical_hist_coll.delete_many({"uuid": {"$in":uuid_list}})
demographic_data_coll.delete_many({"uuid": {"$in":uuid_list}})