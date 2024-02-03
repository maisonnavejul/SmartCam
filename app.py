#SmartCam
import paho.mqtt.client as mqtt
import json
from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from database import insert_data, all_data


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return 'SmartCam Server is running :)'

@app.route('/sendtemperature', methods=['POST'])
def temperature():
    data = request.get_json()
    print(data)
    return jsonify(data)
@app.route('/insertdataTEST', methods=['GET'])
def insertdata():
    insert_data()
    return 'Data inserted successfully.'

@app.route('/getdata', methods=['GET'])
def allData():
    data = all_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='192.168.1.52', port=5000)
