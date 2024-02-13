import sqlite3
import datetime
import random

def create_database():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS info_salle_1 ( id INTEGER PRIMARY KEY, nbpers TEXT DEFAULT '0', temperature TEXT DEFAULT '0', humidity TEXT DEFAULT '0', light TEXT DEFAULT 'OFF',chauffage TEXT DEFAULT 'OFF',chauffage_from_front TEXT DEFAULT 'NO', date TEXT)")
        conn.close()
        print("Database created successfully.")
    except Exception as e:
        print("Error creating database:", str(e))
        
def insert_data(nbpers, temperature, humidity, light, chauffage, chauffage_from_front):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Insertion d'une ligne de données
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO info_salle_1 (nbpers, temperature, humidity, light,chauffage, chauffage_from_front, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (nbpers, temperature, humidity, light, chauffage, chauffage_from_front, now))
        
        conn.commit()  
        conn.close()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error inserting data:", str(e))
        
def all_data():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM info_salle_1 ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching data:", str(e))
        return None

if __name__ == '__main__':
    create_database()