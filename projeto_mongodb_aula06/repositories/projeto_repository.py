from pymongo import InsertOne
from pymongo.errors import BulkWriteError
from models.projeto import Projeto


class ProjetoRepository:
    """
    Repository Pattern para a coleção 'projetos' no MongoDB.
    Centraliza todas as operações de CRUD relacionadas a Projeto,
    promovendo separação de responsabilidades e fácil manutenção.
    """

    COLLECTION_NAME = "projetos"

    def __init__(self, database):
        """
        Inicializa o repositório com a instância do banco de dados.

        :param database: Instância do banco retornada por MongoClient[db_name]
        """
        self.collection = database[self.COLLECTION_NAME]

    # ------------------------------------------------------------------
    # insert_one
    # ------------------------------------------------------------------
    def insert_one(self, projeto: Projeto) -> str:
        """
        Insere um único documento na coleção após validação.

        :param projeto: Instância de Projeto
        :return: ID (str) do documento inserido
        :raises ValueError: se a validação falhar
        """
        projeto.validate()
        resultado = self.collection.insert_one(projeto.to_dict())
        return str(resultado.inserted_id)

    # ------------------------------------------------------------------
    # insert_many
    # ------------------------------------------------------------------
    def insert_many(self, projetos: list) -> list:
        """
        Insere uma lista de documentos na coleção após validar cada um.

        :param projetos: Lista de instâncias de Projeto
        :return: Lista de IDs (str) dos documentos inseridos
        :raises ValueError: se qualquer projeto falhar na validação
        """
        if not projetos:
            raise ValueError("A lista de projetos não pode ser vazia.")

        documentos = []
        for i, projeto in enumerate(projetos):
            try:
                projeto.validate()
                documentos.append(projeto.to_dict())
            except ValueError as e:
                raise ValueError(f"Erro no projeto [{i}] '{projeto.nome}': {e}")

        resultado = self.collection.insert_many(documentos)
        ids = [str(oid) for oid in resultado.inserted_ids]
        print(f"\n✅ {len(ids)} documentos inseridos com sucesso!")
        return ids

    # ------------------------------------------------------------------
    # insert_bulk
    # ------------------------------------------------------------------
    def insert_bulk(self, operacoes: list) -> dict:
        """
        Executa operações em lote usando bulk_write para maior performance.
        Ideal quando há muitos documentos ou operações mistas (insert + update).

        :param operacoes: Lista de objetos pymongo (InsertOne, UpdateOne, etc.)
        :return: Dicionário com o resumo do resultado (inserted_count, etc.)
        :raises BulkWriteError: se alguma operação falhar
        """
        if not operacoes:
            raise ValueError("A lista de operações bulk não pode ser vazia.")

        try:
            resultado = self.collection.bulk_write(operacoes, ordered=False)
            resumo = {
                "inserted_count": resultado.inserted_count,
                "matched_count": resultado.matched_count,
                "modified_count": resultado.modified_count,
                "deleted_count": resultado.deleted_count,
            }
            print(f"\n✅ Bulk write concluído: {resumo}")
            return resumo
        except BulkWriteError as bwe:
            print(f"\n❌ Erro no bulk_write: {bwe.details}")
            raise
