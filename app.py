#SmartCam
import paho.mqtt.client as mqtt
import json
from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from database import *


app = Flask(__name__)
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_client = mqtt.Client()

nbpers = None
temperature = None
humidity = None
light = "OFF"
chauffage = "OFF"
chauffage_from_front = "NO"
want_temperature = None
insert_data_temperature(want_temperature)

bouton_active = False

def on_connect(client, userdata, flags, rc):
    print("Connexion au broker MQTT établie avec le code de retour : " + str(rc))
    client.subscribe("smartcam/data")
    print("Souscription au topic 'smartcam/data'")
    
def on_message(client, userdata, msg):
    global nbpers, temperature, humidity 
    try:
        message_data = json.loads(msg.payload.decode())
        
        if message_data['type'] == 'all_data':
            data = message_data['data']
            print(f"Message général reçu : {data['message']}")
            print(f"Température mise à jour : {data['temperature']}")
            print(f"Humidité mise à jour : {data['humidity']}")
            print(f"Nombre de personnes mis à jour : {data['nbpers']}")
            
            nbpers = data['nbpers']
            temperature = data['temperature']
            humidity = data['humidity']
            
            if None not in (nbpers, temperature, humidity):
                algo(nbpers, temperature, humidity)
                nbpers = None
                temperature = None
                humidity = None
    

            
    except json.JSONDecodeError:
        print("Le message reçu n'est pas un JSON valide.")
    except ValueError as e:
        print("Erreur lors de la conversion du message : ", e)
    except KeyError as e:
        print("Clé manquante dans le message JSON : ", e)
    except TypeError as e:
        print("Erreur de type de données : ", e)


    
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.loop_start()


CORS(app)

def algo(nbpers, temperature, humidity):
    
    chauffage_from_front = last_data_chauffage_from_front()
    
    want_temperature_data = last_data_temperature()
    if want_temperature_data is not None:
        try:
            want_temperature = float(want_temperature_data)  
        except ValueError:
            print("Erreur: la température souhaitée n'est pas un nombre valide.")
            return
    else:
        want_temperature = None
    


    
    print("Chauffage from front: ", chauffage_from_front)
    if chauffage_from_front == "NO":    
        if temperature <= 17:
            chauffage = "ON"
        else:
            chauffage = "OFF"
        if nbpers > 0 :
            light = "ON"
        else:
            light = "OFF"
            
        print('temperature voulue',want_temperature)
        
        if want_temperature is not None:
            if want_temperature >= temperature:
                chauffage = "ON"
                print(want_temperature, '>=', temperature)
            elif want_temperature <= temperature:
                chauffage = "OFF"
                print(want_temperature, '<=', temperature)

        insert_data(nbpers, temperature, humidity, light, chauffage)
        print("Nbper: ", nbpers , "Temperature: ", temperature, "Humidity: ", humidity, "Light: ", light, "Chauffage: ", chauffage, "Chauffage from front: ", chauffage_from_front)
    if chauffage_from_front == "YES":
        if temperature >= 24:
            chauffage = "OFF"
        else:
            chauffage = "ON"
        if nbpers > 0 :
            light = "ON"
        else:
            light = "OFF"
        insert_data(nbpers, temperature, humidity, light, chauffage)
        print("Nbper: ", nbpers , "Temperature: ", temperature, "Humidity: ", humidity, "Light: ", light, "Chauffage: ", chauffage, "Chauffage from front: ", chauffage_from_front)
            
    
    
@app.route('/', methods=['GET'])
def index():
    return 'SmartCam Server is running :)'

@app.route('/sendtemperature', methods=['POST'])
def post_temperature():

    data = request.get_json()
    print(data)
    want_temperature = data['temperature']
    insert_data_temperature(want_temperature)
    return jsonify(data)

@app.route('/test', methods=['GET'])
def test():
    chauffage_from_front = last_data_chauffage_from_front()
    return jsonify({"chauffage_from_front": chauffage_from_front})


@app.route('/sendchauffage', methods=['POST'])
def post_chauffage():

    data = request.get_json()
    print(data)
    chauffage_from_front = data['chauffage']
    print("Chauffage from front send: ", chauffage_from_front)

    
    insert_data_chauffage(chauffage_from_front)

    return jsonify(data)

@app.route('/insertdataTEST', methods=['GET'])
def insertdata():
    print("Inserting data...")
    print("Nbper: ", nbpers , "Temperature: ", temperature, "Humidity: ", humidity, "Light: ", light, "Chauffage: ", chauffage, "Chauffage from front: ", chauffage_from_front)
    insert_data(nbpers, temperature, humidity, light, chauffage)
    return 'Data inserted successfully.'

@app.route('/getdata', methods=['GET'])
def allData():
    data = all_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='10.224.0.83', port=5000)  

