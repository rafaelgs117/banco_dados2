import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
    """Retorna a instância do banco de dados MongoDB."""
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB", "aula06_db")
    client = MongoClient(uri)
    return client[db_name]
