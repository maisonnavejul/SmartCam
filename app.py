#SmartCam
import paho.mqtt.client as mqtt
import json
from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from database import *
import threading
import time

app = Flask(__name__)
CORS(app)

# Configuration MQTT
mqtt_broker_smartcam = "test.mosquitto.org"
mqtt_broker_frigate = "10.222.9.191"
mqtt_port = 1883
mqtt_topic_smartcam = "smartcam/data"
mqtt_topic_frigate = 'frigate/events'

# Clients MQTT
mqtt_client_smartcam = mqtt.Client()
mqtt_client_frigate = mqtt.Client()


nbpers = 0
temperature = None
humidity = None
light = "OFF"
chauffage = "OFF"
chauffage_from_front = "NO"
want_temperature = None
insert_data_temperature(want_temperature)

bouton_active = False



lock = threading.Lock()
last_detection_time = None
timeout_seconds = 10  # Nombre de secondes avant la réinitialisation de nbpers

def check_for_timeout():
    global nbpers, last_detection_time
    while True:
        with lock:
            if last_detection_time and (datetime.datetime.now() - last_detection_time).total_seconds() > timeout_seconds:
                nbpers = 0
                last_detection_time = None
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 0")
        time.sleep(1)

def on_connect_smartcam(client, userdata, flags, rc):
    print("Connecté au broker SmartCam avec le code :", rc)
    client.subscribe(mqtt_topic_smartcam)

def on_connect_frigate(client, userdata, flags, rc):
    print("Connecté au broker Frigate avec le code :", rc)
    client.subscribe(mqtt_topic_frigate)

def on_message_smartcam(client, userdata, msg):
    global temperature, humidity, nbpers
    try:
        # Analyse le message JSON reçu
        message_data = json.loads(msg.payload.decode())
        
        # Vérifie si le message est du type attendu
        if message_data['type'] == 'all_data':
            data = message_data['data']
            
            # Mise à jour des variables globales avec les données reçues
            temperature = data['temperature']
            humidity = data['humidity']
            
            print(f"Message général reçu : {data['message']}")
            print(f"Température mise à jour : {temperature}")
            print(f"Humidité mise à jour : {humidity}")
            print(f"Nombre de personnes (dernière détection) : {nbpers}")
            
            # Exécute la logique d'application basée sur les données mises à jour
            # Par exemple, mise à jour de la base de données ou ajustement des contrôles de l'environnement
            algo(nbpers, temperature, humidity)
            
    except json.JSONDecodeError:
        print("Le message reçu n'est pas un JSON valide.")
    except KeyError as e:
        print(f"Clé manquante dans le message JSON : {e}")
    except (ValueError, TypeError) as e:
        print(f"Erreur lors de la conversion du message : {e}")


def on_message_frigate(client, userdata, msg):
    global nbpers, last_detection_time
    with lock:
        nbpers = 1  # Une détection entraîne nbpers à 1
        last_detection_time = datetime.datetime.now()
        print(f"{last_detection_time.strftime('%Y-%m-%d %H:%M:%S')} - 1")

# Configuration des callbacks MQTT
mqtt_client_smartcam.on_connect = on_connect_smartcam
mqtt_client_smartcam.on_message = on_message_smartcam

mqtt_client_frigate.on_connect = on_connect_frigate
mqtt_client_frigate.on_message = on_message_frigate

# Connexion aux brokers MQTT
mqtt_client_smartcam.connect(mqtt_broker_smartcam, mqtt_port, 60)
mqtt_client_frigate.connect(mqtt_broker_frigate, mqtt_port, 60)

# Démarrage des clients MQTT dans des threads séparés
mqtt_client_smartcam.loop_start()
mqtt_client_frigate.loop_start()

# Démarrer le thread de vérification de timeout
timeout_thread = threading.Thread(target=check_for_timeout)
timeout_thread.daemon = True
timeout_thread.start()


CORS(app)

def publish_led_state(state):
    """
    Publie l'état de la LED ('ON' ou 'OFF') au topic MQTT "smartcam/led".
    """
    mqtt_client_smartcam.publish("smartcam/led", state)
    print(f"État de la LED publié : {state}")

def algo(nbpers, temperature, humidity):
    global light
    
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
            publish_led_state("ON")
        else:
            light = "OFF"
            publish_led_state("OFF")
            
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
            publish_led_state("ON")
        else:
            light = "OFF"
            publish_led_state("OFF")
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
    app.run(host='10.222.9.191', port=5000)  

