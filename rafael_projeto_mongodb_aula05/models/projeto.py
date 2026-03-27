# models/projeto.py
from datetime import datetime
from bson import ObjectId


class Projeto:
    
    # coleçao no MongoDB
    COLECAO = "projetos"

    def __init__(
        self,
        nome: str,
        descricao: str,
        responsavel: str,
        status: str = "planejamento",
        tecnologias: list = None,
        ativo: bool = True,
        _id=None,
    ):
        """
        inicializa um novo Projeto com os campos. 

        Args:
            nome        : Nome do projeto
            descricao   : Descrição detalhada do projeto
            responsavel : Nome do responsável pelo projeto
            status      : Status atual ('planejamento', 'em_andamento', 'concluido', 'cancelado')
            tecnologias : Lista de tecnologias utilizadas
            ativo       : Indica se o projeto está ativo
            _id         : ID do documento (gerado automaticamente pelo MongoDB)
        """
        self._id = _id or ObjectId()
        self.nome = nome
        self.descricao = descricao
        self.responsavel = responsavel
        self.status = status
        self.tecnologias = tecnologias or []
        self.ativo = ativo
        self.criado_em = datetime.now()
        self.atualizado_em = datetime.now()

    def to_dict(self) -> dict:
        """
        Converte o objeto Projeto em um dicionário para inserção no MongoDB.
        """
        return {
            "_id": self._id,
            "nome": self.nome,
            "descricao": self.descricao,
            "responsavel": self.responsavel,
            "status": self.status,
            "tecnologias": self.tecnologias,
            "ativo": self.ativo,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Projeto":
        """
        Cria uma instância de Projeto a partir de um dicionário (documento MongoDB).

        Args:
            dados: Dicionário com os dados do documento

        Returns:
            Instância de Projeto
        """
        projeto = cls(
            nome=dados.get("nome", ""),
            descricao=dados.get("descricao", ""),
            responsavel=dados.get("responsavel", ""),
            status=dados.get("status", "planejamento"),
            tecnologias=dados.get("tecnologias", []),
            ativo=dados.get("ativo", True),
            _id=dados.get("_id"),
        )
        # Preserva as datas originais se existirem
        if "criado_em" in dados:
            projeto.criado_em = dados["criado_em"]
        if "atualizado_em" in dados:
            projeto.atualizado_em = dados["atualizado_em"]
        return projeto

    def __repr__(self) -> str:
        return (
            f"Projeto(id={self._id}, nome='{self.nome}', "
            f"status='{self.status}', responsavel='{self.responsavel}')"
        )

    def __str__(self) -> str:
        return (
            f"📁 Projeto: {self.nome}\n"
            f"   Descrição  : {self.descricao}\n"
            f"   Responsável: {self.responsavel}\n"
            f"   Status     : {self.status}\n"
            f"   Tecnologias: {', '.join(self.tecnologias) if self.tecnologias else 'N/A'}\n"
            f"   Ativo      : {'Sim' if self.ativo else 'Não'}\n"
            f"   Criado em  : {self.criado_em.strftime('%d/%m/%Y %H:%M')}"
        )
