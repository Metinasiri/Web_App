import json
import pusher
import pymongo
from bson import json_util
from flask import Flask, jsonify

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://piryadevi:pakistan123@smartdiaper.uvlojw5.mongodb.net/?retryWrites=true"
                               "&w=majority")
mydb = myclient["smartdiaper"]
mycol = mydb["patient_data"]
pusher_client = pusher.Pusher(
    app_id='1573905',
    key='04baa22ea6e8b380ff7b',
    secret='237abc93fa545c60dc17',
    cluster='eu',
    ssl=True,
)


#@app.route('/diaper-data')
# def fetch_data():
#     x = mycol.find_one()
#     y = mycol.find()
#     for data in y:
#         print(data)


#fetch_data()
cursor = mycol.watch(full_document='updateLookup')
print(cursor)
for document in cursor:
    print(document, 'document') # print for reference, 'document' for reference
    if 'Volume' in document['fullDocument']:
        fullness = document['fullDocument']['Volume']
        passedTime = document['fullDocument']['Passed Time']
        batteryStatus = document['fullDocument']['Battery Status']
        # Determine the diaper alert level based on the fullness level
        if fullness >= 90:
            patient_name = document['fullDocument']['Name']
            message = 'Urgent: change diaper now!'
            urine_volume = fullness
            Room = document['fullDocument']['Room']
            changedDiaper = document['fullDocument']['Changed Diaper']
            passedTime = passedTime
            batteryStatus = batteryStatus
            alert_class = 'urgent'
            column_class = 'red'
        elif fullness >= 60 < 90:
            patient_name = document['fullDocument']['Name']
            message = 'Change diaper soon'
            urine_volume = fullness
            Room = document['fullDocument']['Room']
            changedDiaper = document['fullDocument']['Changed Diaper']
            passedTime = passedTime
            batteryStatus = batteryStatus
            alert_class = 'warning'
            column_class = 'yellow'
        else:
            patient_name = document['fullDocument']['Name']
            message = 'Diaper is okay'
            urine_volume = fullness
            Room = document['fullDocument']['Room']
            changedDiaper = document['fullDocument']['Changed Diaper']
            passedTime = passedTime
            batteryStatus = batteryStatus
            alert_class = ''
            column_class = 'green'

        # Trigger a Pusher event to update the diaper alert in the browser
        pusher_client.trigger('my-channel', 'my-event', {
            'id' : document['fullDocument']['_id'],
            'Name': patient_name,
            'Volume': fullness,
            'message': message,
            'class': alert_class,
            'column': column_class,
            'Room': document['fullDocument']['Room'],
            'ChangedDiaper': document['fullDocument']['Changed Diaper'],
            'passedTime': passedTime,
            'batteryStatus': batteryStatus,
        })
# with mycol.watch() as stream: ## sending notification tried this code.
#     for change in stream:
#         # Trigger Pusher event for each change
#         data = json.loads(json_util.dumps(change['fullDocument']))
#         # pusher_client.trigger('smart_testing', 'my_event', {'message': 'hello'})
#         # print(response)
#         pusher_client.trigger('my-channel', 'my-event', {'message': data})
