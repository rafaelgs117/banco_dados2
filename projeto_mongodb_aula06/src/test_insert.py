##Seu Nome
import sys
import os

# Garante que o diretório raiz do projeto esteja no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymongo import InsertOne
from config.db import get_database
from models.projeto import Projeto
from repositories.projeto_repository import ProjetoRepository


def main():
    print("=" * 60)
    print("  AULA 06 - PyMongo: Repository Pattern e Inserção de Dados")
    print("=" * 60)

    # Conexão com o banco
    db = get_database()
    repo = ProjetoRepository(db)

    # ------------------------------------------------------------------
    # 1. Instanciar 10 projetos fictícios
    # ------------------------------------------------------------------
    projetos = [
        Projeto(
            nome="Sistema de E-commerce",
            descricao="Plataforma de vendas online com carrinho e pagamento.",
            status="ativo",
            tecnologias=["Python", "Django", "PostgreSQL", "React"],
        ),
        Projeto(
            nome="App de Finanças Pessoais",
            descricao="Controle de receitas, despesas e metas financeiras.",
            status="em_andamento",
            tecnologias=["Flutter", "Firebase", "Dart"],
        ),
        Projeto(
            nome="API REST de Autenticação",
            descricao="Serviço de autenticação com JWT e OAuth2.",
            status="concluido",
            tecnologias=["Node.js", "Express", "MongoDB", "JWT"],
        ),
        Projeto(
            nome="Dashboard Analítico",
            descricao="Painel de BI com gráficos em tempo real.",
            status="ativo",
            tecnologias=["Python", "FastAPI", "Vue.js", "Chart.js"],
        ),
        Projeto(
            nome="Chatbot de Atendimento",
            descricao="Bot para suporte ao cliente via WhatsApp.",
            status="em_andamento",
            tecnologias=["Python", "Twilio", "NLP", "MongoDB"],
        ),
        Projeto(
            nome="Sistema de Gestão Escolar",
            descricao="Controle de alunos, turmas, notas e frequência.",
            status="pausado",
            tecnologias=["Java", "Spring Boot", "MySQL", "Angular"],
        ),
        Projeto(
            nome="Plataforma de Streaming",
            descricao="Serviço de vídeos sob demanda com assinatura.",
            status="ativo",
            tecnologias=["Go", "Kubernetes", "Redis", "React"],
        ),
        Projeto(
            nome="Rede Social de Desenvolvedores",
            descricao="Comunidade para compartilhar projetos e snippets.",
            status="em_andamento",
            tecnologias=["Python", "Django", "PostgreSQL", "Bootstrap"],
        ),
        Projeto(
            nome="IoT - Monitoramento Agrícola",
            descricao="Sensores para controle de irrigação e clima.",
            status="ativo",
            tecnologias=["C++", "MQTT", "Python", "InfluxDB"],
        ),
        Projeto(
            nome="Marketplace de Freelancers",
            descricao="Plataforma para contratação de profissionais de TI.",
            status="concluido",
            tecnologias=["Ruby on Rails", "PostgreSQL", "Stripe", "React"],
        ),
    ]

    # ------------------------------------------------------------------
    # 2. Inserção em massa com insert_many
    # ------------------------------------------------------------------
    print("\n📦 Inserindo 10 projetos via insert_many()...\n")
    ids = repo.insert_many(projetos)

    print("\n📋 IDs dos documentos inseridos:")
    for i, doc_id in enumerate(ids, start=1):
        print(f"  [{i:02d}] {doc_id}")

    # ------------------------------------------------------------------
    # 3. Demonstração de validação com dado inválido (proposital)
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  TESTE DE VALIDAÇÃO - Inserção com dado inválido")
    print("=" * 60)

    projeto_invalido = Projeto(
        nome="",          # nome vazio → deve falhar
        descricao="Projeto sem nome",
        status="ativo",
        tecnologias=["Python"],
    )

    try:
        repo.insert_one(projeto_invalido)
    except ValueError as e:
        print(f"\n❌ Erro de validação capturado corretamente:\n   {e}")

    # ------------------------------------------------------------------
    # 4. Demonstração de insert_bulk (bulk_write)
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  DEMONSTRAÇÃO - insert_bulk (bulk_write)")
    print("=" * 60)

    projetos_bulk = [
        Projeto(
            nome="Projeto Bulk A",
            descricao="Teste de bulk_write - operação A.",
            status="ativo",
            tecnologias=["Python", "MongoDB"],
        ),
        Projeto(
            nome="Projeto Bulk B",
            descricao="Teste de bulk_write - operação B.",
            status="inativo",
            tecnologias=["JavaScript", "Node.js"],
        ),
    ]

    operacoes = [InsertOne(p.to_dict()) for p in projetos_bulk]
    print("\n⚙️  Executando bulk_write com 2 operações...")
    resumo = repo.insert_bulk(operacoes)
    print(f"   Resultado: {resumo}")

    print("\n✅ Script finalizado com sucesso!\n")


if __name__ == "__main__":
    main()
