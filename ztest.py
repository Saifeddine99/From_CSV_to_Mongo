from pymongo import MongoClient

from encrypt import encrypt_data
from decrypt import decrypt_data

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

decision= input("Choose between storing/ querying: ")

if decision=="store":

    # Insert a document with encrypted data as strings
    name= input("Enter the name to store: ")
    age= input("Enter the age to store: ")
    city= input("Enter the city to store: ")
    data_to_insert = {
        "name": encrypt_data(name),
        "age": encrypt_data(age),
        "city": encrypt_data(city)
    }

    collection.insert_one(data_to_insert)
    print("Document added to database.")


elif decision=="query":
    # Query documents where the decrypted 'name' is 'Alice'
    query_by_name=input("Enter the name to query: ")
    encrypted_value = encrypt_data(query_by_name)

    query_condition = {"name": encrypted_value}

    result = collection.find_one(query_condition)

    # Decrypt and print the values
    if result:

        decrypted_name = decrypt_data(result["name"])
        decrypted_age = decrypt_data(result["age"])
        decrypted_city = decrypt_data(result["city"])

        print("Decrypted Data:")
        print("Name:", decrypted_name)
        print("Age:", decrypted_age)
        print("City:", decrypted_city)

    else:
        print("No matching document found.")

else:

    ciphertext=encrypt_data("Alice")
    print(f"ciphertext: {ciphertext}")

    originaltext=decrypt_data(ciphertext)
    print(f"Original text: {originaltext}")