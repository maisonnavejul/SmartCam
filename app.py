#SmartCam
import paho.mqtt.client as mqtt
import json
from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from database import *


app = Flask(__name__)


CORS(app)

nbper = 0
temperature = 20
humidity = 12
light = "OFF"
chauffage = "OFF"
chauffage_from_front = "NO"


@app.route('/', methods=['GET'])
def index():
    return 'SmartCam Server is running :)'

@app.route('/sendtemperature', methods=['POST'])
def post_temperature():
    data = request.get_json()
    print(data)
    return jsonify(data)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"chauffage_from_front": chauffage_from_front})

#recupération chauffage from front
@app.route('/sendchauffage', methods=['POST'])
def post_chauffage():
    global chauffage_from_front
    data = request.get_json()
    print(data)
    chauffage_from_front = data['chauffage']
    #insert_data(nbper, temperature, humidity, light, chauffage, chauffage_from_front)
    return jsonify(data)

@app.route('/insertdataTEST', methods=['GET'])
def insertdata():
    print("Inserting data...")
    print("Nbper: ", nbper , "Temperature: ", temperature, "Humidity: ", humidity, "Light: ", light, "Chauffage: ", chauffage, "Chauffage from front: ", chauffage_from_front)
    insert_data(nbper, temperature, humidity, light, chauffage, chauffage_from_front)
    return 'Data inserted successfully.'

@app.route('/getdata', methods=['GET'])
def allData():
    data = all_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='10.224.0.99', port=5000)

