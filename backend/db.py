import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="corazon71",
        database="voiceup_ai"
    )
