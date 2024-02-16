import paho.mqtt.client as mqtt
import json

# Fonction appelée suite à chaque publication
def on_publish(client, userdata, mid):
    print("Message publié")

# Configuration du client MQTT pour la publication
client = mqtt.Client()

# Assignation de la fonction de rappel
client.on_publish = on_publish

# Connexion au broker
client.connect("test.mosquitto.org", 1883, 60)

# Démarrage de la boucle
client.loop_start()

# Préparation des données
data = {
    "type": "all_data",
    "data": {
        "message": "Hello World",
        "temperature": 18,
        "humidity": 50,
        "nbpers": 0
    }
}

# Conversion des données en JSON et publication
client.publish("smartcam/data", json.dumps(data))

# Arrêt de la boucle après la publication
client.loop_stop()

# Déconnexion du broker
client.disconnect()
