# config/database.py
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()


class DatabaseManager:
    """
    Gerencia a conexão com o banco de dados MongoDB.
    Implementa o padrão Singleton para garantir uma única conexão.
    """

    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        """Garante que apenas uma instância seja criada (Singleton)."""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def conectar(self):
        """
        Estabelece a conexão com o MongoDB usando a URI do .env.
        Retorna True se bem-sucedido, False caso contrário.
        """
        try:
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
            db_name = os.getenv("MONGO_DB_NAME", "aula05_db")

            self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

            # Testa a conexão imediatamente
            self._client.admin.command("ping")

            self._db = self._client[db_name]

            print(f"✅ Conexão estabelecida com sucesso!")
            print(f"   URI: {mongo_uri}")
            print(f"   Banco: {db_name}")
            return True

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ Falha ao conectar ao MongoDB: {e}")
            return False

    def desconectar(self):
        """Fecha a conexão com o MongoDB."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("🔌 Conexão encerrada.")

    def get_database(self):
        """Retorna a instância do banco de dados ativo."""
        if self._db is None:
            raise RuntimeError("Banco de dados não conectado. Execute conectar() primeiro.")
        return self._db

    def get_client(self):
        """Retorna o cliente MongoDB."""
        if self._client is None:
            raise RuntimeError("Cliente não inicializado. Execute conectar() primeiro.")
        return self._client

    def listar_databases(self):
        """Lista todos os databases disponíveis no servidor MongoDB."""
        if self._client is None:
            raise RuntimeError("Cliente não inicializado. Execute conectar() primeiro.")

        databases = self._client.list_database_names()
        return databases

    def listar_colecoes(self):
        """Lista todas as coleções do banco de dados ativo."""
        if self._db is None:
            raise RuntimeError("Banco de dados não conectado. Execute conectar() primeiro.")

        colecoes = self._db.list_collection_names()
        return colecoes

    @property
    def db(self):
        """Propriedade de atalho para acessar o banco de dados."""
        return self.get_database()
