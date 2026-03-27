# imports
import sys
import os

# garante diretório raiz do projeto 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import DatabaseManager
from models.projeto import Projeto


def exibir_separador(titulo: str = ""):
    """Exibe um separador visual no terminal."""
    linha = "=" * 55
    if titulo:
        print(f"\n{linha}")
        print(f"  {titulo}")
        print(linha)
    else:
        print(linha)


def listar_databases(db_manager: DatabaseManager):
    """Lista todos os databases disponíveis no servidor."""
    exibir_separador("📂 Databases Disponíveis no Servidor")

    databases = db_manager.listar_databases()

    if databases:
        for i, nome_db in enumerate(databases, start=1):
            print(f"  {i}. {nome_db}")
    else:
        print("  Nenhum database encontrado.")

    print(f"\n  Total: {len(databases)} database(s)")


def main():
    """Função principal do script."""
    print("\n" + "=" * 55)
    print("  🚀 AULA 05 — Estruturando Meu Projeto PyMongo")
    print("=" * 55)

    # 1 - gerencia de conexao
    db_manager = DatabaseManager()

    # 2 - estabelece a conexao
    exibir_separador("🔌 Conectando ao MongoDB")
    conectado = db_manager.conectar()

    if not conectado:
        print("\n⚠️  Não foi possível conectar ao MongoDB.")
        print("   Verifique se o serviço está rodando e a URI no .env está correta.")
        print("\n   Continuando com demonstração do modelo...\n")
        demonstrar_modelo()
        return

    # 3 - lista todos os meus bancos no mongo
    listar_databases(db_manager)

    #4 -  fecha conexao
    exibir_separador("👋 Encerrando")
    db_manager.desconectar()
    print("\n✅ Script finalizado com sucesso!\n")


if __name__ == "__main__":
    main()
