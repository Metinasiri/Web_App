import json
import pusher
import pymongo
from bson import json_util
from flask import Flask, jsonify

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://<mongoDBUserName>:<MongoDbPWD>@smartdiaper.uvlojw5.mongodb.net"
                               " /?retryWrites=true "
                               "&w=majority")
mydb = myclient["smartdiaper"]
# mycol = mydb["patient_data"]
mycol = mydb["info_patient"]
pusher_client = pusher.Pusher(
    app_id='1573905',
    key='04baa22ea6e8b380ff7b',
    secret='237abc93fa545c60dc17',
    cluster='eu',
    ssl=True,
)

from bson import json_util


@app.route('/diaper-data')
def fetch_data():
    x = mycol.find_one()
    y = mycol.find({}, {"admission_date": "2023-05-28"})
    # for j in mycol.find({},{ "admission_date": "2023-05-28"}):
    #    print(j)
    # print('jhhdsfkhjdfhjsdjfhdsgdsgfjkhgsdjfjsdfgjsdfj')
    # for data in y:
    #    print(data)


# fetch_data()
cursor = mycol.watch(full_document='updateLookup')
for document in cursor:
    print(document, 'document')  # print for reference, 'document' for reference
    mac_address = document['fullDocument']['MACAddress']
    if mac_address == "F4:12:FA:86:6E:50":
        # if 'Volume' in document['fullDocument']:
        fullness = document['fullDocument']['Voltage']
        # passedTime = document['fullDocument']['Passed Time']
        # batteryStatus = document['fullDocument']['BatteryStatus']
        # Determine the diaper alert level based on the fullness level
        mac_address = document['fullDocument']['MACAddress']
        battery_status = document['fullDocument']['BatteryStatus']

        voltage = fullness  # Provide the value for voltage variable
        volumeCalc = (108.894510 * voltage ** 3 + 93.2517375 * voltage ** 2 + 0.0402301727 * voltage + 1.83609292)
        volume = float("{:.2f}".format(volumeCalc))
        print(type(volume))
        # Calculate the percentage volume
        percentVolume = volume / 700 * 100
        percentageOfVolume = "{:.2f}".format(percentVolume)

        print("Percentage Volume:", percentageOfVolume)

        if volume >= 400:
            patient_name = 'Jukka'  # document['fullDocument']['Name']
            message = 'Urgent: change diaper now!'
            urine_volume = volume
            Room = 14  # document['fullDocument']['Room']
            mac_address = mac_address  # document['fullDocument']['MACAddress']
            battery_status = battery_status  # document['fullDocument']['BatteryStatus']
            # changedDiaper = document['fullDocument']['Changed Diaper']
            # passedTime = passedTime
            # batteryStatus = batteryStatus
            alert_class = 'urgent'
            column_class = 'red'
        elif volume >= 200 < 400:
            patient_name = 'Jukka'  # document['fullDocument']['Name']
            message = 'Change diaper soon!'
            urine_volume = volume
            Room = 14  # document['fullDocument']['Room']
            mac_address = mac_address  # document['fullDocument']['MACAddress']
            battery_status = battery_status  # document['fullDocument']['BatteryStatus']
            # changedDiaper = document['fullDocument']['Changed Diaper']
            # passedTime = passedTime
            # batteryStatus = batteryStatus
            alert_class = 'warning'
            column_class = 'yellow'
        else:
            patient_name = 'Jukka'  # document['fullDocument']['Name']
            message = 'Diaper is okay!'
            urine_volume = volume
            Room = 14  # document['fullDocument']['Room']
            mac_address = mac_address  # document['fullDocument']['MACAddress']
            battery_status = battery_status  # document['fullDocument']['BatteryStatus']
            # changedDiaper = document['fullDocument']['Changed Diaper']
            # passedTime = passedTime
            # batteryStatus = batteryStatus
            alert_class = ''
            column_class = 'green'

        # voltage = 1.1  # Provide the value for voltage variable
        #
        # volume = 883.06545396 * voltage ** 3 - 2226.65005473 * voltage ** 2 + 1718.56019027 * voltage - 242.57131415
        # print("Volume:", volume)
        #
        # # Calculate the percentage volume
        # percentVolume = (volume / 700) * 100
        # print("Percentage Volume:", percentVolume)

        # Trigger a Pusher event to update the diaper alert in the browser
        data = {
            # 'id': document['fullDocument']['_id'],
            'Name': 'Jukka',  # patient_name,
            'Volume': volume,
            'battery_status': battery_status,
            'mac_address': mac_address,
            'percentage_volume' : percentageOfVolume,
            'message': message,
            'class': alert_class,
            'column': column_class,
            'Room': '14',
        }
        mycol.update_one({'_id': document['fullDocument']['_id']}, {'$set': data})
        pusher_client.trigger('my-channel', 'my-event', data

                              # {
                              #     'id': document['fullDocument']['_id'],
                              #     'Name': 'Jukka',#patient_name,
                              #     'Volume': fullness,
                              #     'battery_status': battery_status,
                              #     'mac_address': mac_address,
                              #     'message': message,
                              #     'class': alert_class,
                              #     'column': column_class,
                              #     'Room': '14',#document['fullDocument']['Room'],
                              #     #'ChangedDiaper': document['fullDocument']['Changed Diaper'],
                              #     #'passedTime': passedTime,
                              #     #'batteryStatus': batteryStatus,}
                              )
        # document['fullDocument']['Room'],
        # 'ChangedDiaper': document['fullDocument']['Changed Diaper'],
        # 'passedTime': passedTime,
        # 'batteryStatus': batteryStatus,

# with mycol.watch() as stream: ## sending notification tried this code.
#     for change in stream:
#         # Trigger Pusher event for each change
#         data = json.loads(json_util.dumps(change['fullDocument']))
#         # pusher_client.trigger('smart_testing', 'my_event', {'message': 'hello'})
#         # print(response)
#         pusher_client.trigger('my-channel', 'my-event', {'message': data})
