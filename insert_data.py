from flask import Flask, render_template, request
import pymongo
import logging

app = Flask(__name__)

myclient = pymongo.MongoClient(
    "mongodb+srv://<mongoDBUserName>:<MongoDbPWD>@smartdiaper.uvlojw5.mongodb.net/?retryWrites=true"
    "&w=majority")
mydb = myclient["smartdiaper"]
# mycol = mydb["patient_data"]
mycol = mydb["info_patient"]


def insert_data(data):
    x = mycol.insert_one(data)
    print(x)


logging = logging.getLogger('smart-diaper')


@app.route('/result', methods=['GET', 'POST'])
def result():
    print('HEllo there')
    if request.method == "POST":
        print('i am in POST')
        data_patient = {'patient_name': request.form["patient_name"],
                        'patient_room': request.form["Room"],
                        'deviceId': request.form["deviceId"],
                        'admission_date': request.form['admission_date']
                        }

        print('Inserting')
        print(data_patient)
        insert_data(data_patient)
        # return data_patient
        render_template('index.html', data=data_patient)
    elif request.method == "GET":
        return 'GET method is not supported'

    return data_patient


def update_data(mac_address):
    # newvalues = {"$set": {'quantity': 25}}
    # Updating filter as per your needs.
    filter = {'MACAddress': mac_address}
    # new_values = {"$set": {'Name': 'Jukka', 'Volume': 350, 'Room': 14}}
    new_values = {"$set": {'Volume': 475}}
    try:
        update_data_info = mycol.update_one(filter, new_values)
        if update_data_info.matched_count > 0:
            print("Document updated successfully.")
        else:
            print("No document found with the provided mac_address.")
    except Exception as e:
        print("An error occurred while updating the document:", str(e))
        print(update_data_info)


macAddress = "F4:12:FA:86:6E:50"
# update_data(macAddress)

# data = {"_id": 540, "Name": "jung", "Room": "63", "Volume": 459}
data = {"MACAddress": "F4:12:FA:86:6E:50", "BatteryStatus": "3.051794767", "Voltage": 1.8}
insert_data(data)

if __name__ == "__main__":
    app.run(debug=False)
