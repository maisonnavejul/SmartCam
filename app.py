#SmartCam
import paho.mqtt.client as mqtt
import json
from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'SmartCam Server is running :)'


if __name__ == '__main__':
    app.run(host='10.224.0.99', port=5000)
