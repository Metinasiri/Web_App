import pymongo

myclient = pymongo.MongoClient(
    "mongodb+srv://piryadevi:pakistan123@smartdiaper.uvlojw5.mongodb.net/?retryWrites=true"
    "&w=majority")
mydb = myclient["smartdiaper"]
mycol = mydb["patient_data"]


def insert_data(data):  ## for inserting data
    x = mycol.insert_one(data)
    print(x)


data = {"_id": 549, "Name": "zina", "Room": "44", "Volume": 80, "voltage": 3, "volumePercentage": 35,
        "Changed Diaper": 2, "Passed Time": 3, "deviceId": 3, "Battery Status": "2.8",
        "threshold": 700, "urgency": "soon", "patientStatus": "admitted"}

#insert_data(data)


def update_data(id):
    # newvalues = {"$set": {'quantity': 25}}
    # Updating filter as per your needs.
    filter = {'_id': id}
    new_values = {"$set": {'Name': 'Ziya', 'Room': 48, 'Volume': 80, "voltage": 3}}
    update_data_info = mycol.update_one(filter, new_values)
    print(update_data_info)


update_data(549)
