import random
from datetime import time

import pymongo
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import pusher

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://piryadevi:pakistan123@smartdiaper.uvlojw5.mongodb.net/?retryWrites=true"
                               "&w=majority")
mydb = myclient["smartdiaper"]
mycol = mydb["Patients_info"]
pusher_client = pusher.Pusher(
    app_id='1573905',
    key='04baa22ea6e8b380ff7b',
    secret='237abc93fa545c60dc17',
    cluster='eu',
    ssl=True,
)


# Define routes to retrieve patient information and diaper alert thresholds
@app.route('/patient/<patient_id>')
def get_patient(patient_id):
    patient = mydb.patients.find_one({'_id': patient_id})
    return jsonify(patient)


@app.route('/diaper_threshold/<patient_id>')
def get_diaper_threshold(patient_id):
    threshold = mydb.thresholds.find_one({'patient_id': patient_id})
    return jsonify(threshold)


# Define a route to update the diaper alert threshold
@app.route('/diaper_threshold/<patient_id>', methods=['POST'])
def update_diaper_threshold(patient_id):
    new_threshold = int(request.form['threshold'])
    mydb.thresholds.update_one(
        {'_id': patient_id},
        {'$set': {'threshold': new_threshold}}
    )
    pusher_client.trigger(f'patient-{patient_id}', 'diaper_threshold_updated', {})
    return jsonify({'status': 'success'})


# Define a stream to send diaper alerts in real-time
def diaper_alert_stream(patient_id):
    threshold = mydb.mycol.find_one({'_id': patient_id})
    while True:
        diaper_status = get_diaper_status(patient_id)
        if diaper_status >= threshold:
            pusher_client.trigger(f'patient-{patient_id}', 'diaper_alert', {'status': 'change diaper!'})
        time.sleep(10)


# Define a helper function to get the current diaper status
def get_diaper_status(patient_id):
    # replace with your own logic to get the current diaper status
    return random.randint(0, 100)


if __name__ == '__main__':
    # Start the diaper alert stream in a separate thread
    import threading

    stream_thread = threading.Thread(target=diaper_alert_stream, args=('patient-id',))
    stream_thread.start()

    # Start the Flask app
    app.run(debug=True)
