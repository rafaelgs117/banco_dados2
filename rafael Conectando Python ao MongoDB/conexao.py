import pymongo

# conecxao localhost porta 27017
client = pymongo.MongoClient("mongodb://localhost:27017/")

# lista todos os meus bancos
databases = client.list_database_names()
print("Databases disponíveis:")
for db in databases:
    print(" -", db)

# -----------------------

import pymongo
from datetime import datetime

# conecata com MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# seleciona o banco e colecaoo
db     = client["loja"]
colecao = db["produtos"]

# 5 documentos 
produtos = [
    {
        "nome": "Notebook Dell Inspiron",
        "categoria": "Eletrônicos",
        "valor": 3799.90,
        "ativo": True,
        "data_cadastro": datetime(2024, 1, 10)
    },
    {
        "nome": "Mouse Logitech MX Master",
        "categoria": "Periféricos",
        "valor": 459.00,
        "ativo": True,
        "data_cadastro": datetime(2024, 2, 5)
    },
    {
        "nome": "Teclado Mecânico Redragon",
        "categoria": "Periféricos",
        "valor": 289.99,
        "ativo": True,
        "data_cadastro": datetime(2024, 2, 18)
    },
    {
        "nome": "Monitor 24\" Samsung",
        "categoria": "Eletrônicos",
        "valor": 1299.00,
        "ativo": False,
        "data_cadastro": datetime(2024, 3, 1)
    },
    {
        "nome": "Webcam Full HD Logitech",
        "categoria": "Periféricos",
        "valor": 379.50,
        "ativo": True,
        "data_cadastro": datetime(2024, 3, 15)
    }
]

# insercao documentos
resultado = colecao.insert_many(produtos)

# Confirmação
print(f"✔ Inseridos com sucesso: {len(resultado.inserted_ids)} documentos")
print("IDs gerados:")
for i, id_doc in enumerate(resultado.inserted_ids, 1):
    print(f"  {i}. {id_doc}")

# -----------------------

import pymongo
# conexaoo com o MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")


# seleciona banco
db      = client["loja"]
colecao = db["produtos"]


# busca todos os documentos
produtos = colecao.find()


print("=" * 50)
print("LISTAGEM DE PRODUTOS")
print("=" * 50)


for i, produto in enumerate(produtos, 1):
    print(f"\n[{i}] {produto['nome']}")
    print(f"    Categoria : {produto['categoria']}")
    print(f"    Valor     : R$ {produto['valor']:.2f}")
    print(f"    Ativo     : {produto['ativo']}")
    print(f"    Cadastro  : {produto['data_cadastro'].strftime('%d/%m/%Y')}")
    print(f"    ID        : {produto['_id']}")


print("\n" + "=" * 50)
print(f"Total de registros: {colecao.count_documents({})}")
