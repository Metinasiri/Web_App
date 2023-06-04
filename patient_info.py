from flask import Flask, render_template, request
import pymongo
import logging

app = Flask(__name__)

myclient = pymongo.MongoClient(
    "mongodb+srv://<mongoDBUserName>:<MongoDbPWD>.uvlojw5.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["smartdiaper"]
mycol = mydb["info_patient"]


@app.route('/register/', methods=['POST'])
def patient_info():
    print('jai')
    if request.method == "POST":
        data = {
            'patient_name': request.form["patient_name"],
            'patient_room': request.form["Room"],
            'deviceId': request.form["deviceId"],
            'admission_date': request.form['admission_date']
        }
        logging.error(data)
        try:
            insert_patient_data = mycol.insert_one(data)
            print('data', insert_patient_data)
        except Exception as e:
            print(f"Error inserting data: {e}")
            return "Error inserting data"

        return render_template('index.html', data=data)

    elif request.method == "GET":
        return 'GET method is not supported'
    #return 'data'


if __name__ == "__main__":
    app.debug=True
    app.run()
