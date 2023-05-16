from flask import Flask, render_template, request
import pymongo
import logging

app = Flask(__name__)

myclient = pymongo.MongoClient(
    "mongodb+srv://piryadevi:pakistan123@smartdiaper.uvlojw5.mongodb.net/?retryWrites=true"
    "&w=majority")
mydb = myclient["smartdiaper"]
mycol = mydb["patient_data"]


def insert_data(data):
    x = mycol.insert_one(data)
    print(x)


logging = logging.getLogger('smart-diaper')


@app.route('/register', methods=['GET', 'POST'])
def register_patient():
    print('HEllo there')
    if request.method == "POST":
        print('i am in POST')
        data = {'patient_name': request.form["patient_name"],
                'patient_room': request.form["Room"],
                'deviceId': request.form["deviceId"],
                'admission_date': request.form['admission_date']
                }
        try:
            print('Inserting')
            insert_patient_data = mycol.insert_one(data)
            print('data', insert_patient_data)
        except Exception as e:
            print(f"Error inserting data: {e}")
            return "Error inserting data"
        # print(insert_patient_data)
        # return(f'<h1>{data}</h1>')
        return render_template('index.html', data=data)
    elif request.method == "GET":
        print('get')
        return 'GET method is not supported'

    # return 'ok.'


#     patient_name = request.form["patient_name"]
#     print(patient_name)
#     room = request.form["Room"]
#     device_id = request.form["deviceId"]
#     admission_date = request.form["admission_date"]
#     return render_template('index.html', patient_name=room)
# patient_name = request.form["patient_name"]
# #print(request.args)
# for j in request.data:
#    print(j['patient_name'], 'kkkkk')
# print(type(request.form), 'request method........................')
# if request.method == "GET":
#     print('Yes, the form was submitted')
# patient_name = request.form["patient_name"]
# patient_room = request.form["Room"]
# deviceId = request.form["deviceId"]
# admission_date = request.form['admission_date']
# print(patient_name, patient_room, deviceId, admission_date)
# patient_info = {'patient_name': patient_name}
# , 'Room': patient_room, 'deviceId': deviceId, 'admission_date': admission_date}
# print(patient_info)
# mycol.insert_one(patient_info)
# return 'ok'
# return render_template('index.html', data=patient_info)
# else:
#    print('No, the form was not submitted')
#    return 'No'


# @app.route('/update_data')
def update_data(id):
    # newvalues = {"$set": {'quantity': 25}}
    # Updating filter as per your needs.
    filter = {'_id': id}
    new_values = {"$set": {'Name': 'Sheena', 'Volume': 350, 'Room': 15}}
    update_data_info = mycol.update_one(filter, new_values)
    print(update_data_info)


update_data(548)

data = {"_id": 540, "Name": "jung", "Room": "63", "Volume": 459}
#insert_data(data)

if __name__ == "__main__":
    app.run(debug=False)
