from datetime import datetime


class Projeto:
    """
    Modelo que representa um Projeto no MongoDB.
    Inclui validação de campos obrigatórios e conversão para dicionário.
    """

    CAMPOS_OBRIGATORIOS = ["nome", "descricao", "status"]
    STATUS_VALIDOS = ["ativo", "inativo", "concluido", "em_andamento", "pausado"]

    def __init__(
        self,
        nome: str,
        descricao: str,
        status: str,
        tecnologias: list = None,
        data_cadastro: datetime = None,
    ):
        self.nome = nome
        self.descricao = descricao
        self.status = status
        self.tecnologias = tecnologias if tecnologias is not None else []
        self.data_cadastro = data_cadastro if data_cadastro is not None else datetime.utcnow()

    def validate(self) -> bool:
        """
        Valida os campos obrigatórios e regras de negócio.
        Retorna True se válido, False caso contrário.
        Lança ValueError com mensagem descritiva se inválido.
        """
        # Verifica campos obrigatórios
        for campo in self.CAMPOS_OBRIGATORIOS:
            valor = getattr(self, campo, None)
            if not valor or (isinstance(valor, str) and not valor.strip()):
                raise ValueError(f"Campo obrigatório ausente ou vazio: '{campo}'")

        # Valida status
        if self.status not in self.STATUS_VALIDOS:
            raise ValueError(
                f"Status inválido: '{self.status}'. "
                f"Valores permitidos: {self.STATUS_VALIDOS}"
            )

        # Valida tecnologias
        if not isinstance(self.tecnologias, list):
            raise ValueError("O campo 'tecnologias' deve ser uma lista.")

        return True

    def to_dict(self) -> dict:
        """Retorna dicionário válido para inserção no MongoDB."""
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "status": self.status,
            "tecnologias": self.tecnologias,
            "data_cadastro": self.data_cadastro,
        }

    def __repr__(self):
        return f"<Projeto nome='{self.nome}' status='{self.status}'>"
