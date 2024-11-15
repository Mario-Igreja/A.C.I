import uuid
from models.job import Job
from database import AnalizadorDatabase

# Inicializar a conexão com o banco de dados
database = AnalizadorDatabase()

# Definir informações da vaga
name = 'Vaga de Gestor Comercial de B2B'

activities = '''
Gerenciar o time Comercial
Desenhar estratégias de B2B para escalar o faturamento
Definir e acompanhar metas do B2B com o time
Acompanhar e ajudar o time a executar as estratégias definidas
Reportar resultados e projeções dos seus KPIs
'''

prerequisites = '''
Experiência comprovada como Gestor de Vendas, Líder Comercial, Diretor Comercial ou afins
Experiência comprovada em Vendas B2B (business to business)
Experiência em empresas de Infoprodutos
Proatividade e curiosidade, buscando constantemente aprender e melhorar as habilidades.
Foco em bater as metas estabelecidas para o time de Vendas
Disponibilidade para trabalho em período integral (full time)
'''

differentials = '''
Conhecimento da metodologia VTSD (Leandro Ladeira)
Conhecimento avançado de Funis de Venda, com uma abordagem estratégica e eficaz na aquisição e retenção de clientes
Interesse por Programação e Tecnologia (fique tranquilo, NÃO é necessário saber programar)
Experiência como Gestor Comercial no nicho de Tecnologia em geral, Programação ou Data Science, proporcionando uma compreensão mais profunda do nosso público-alvo
'''

# Verificar se as informações da vaga estão completas
if not all([name, activities, prerequisites, differentials]):
    print("Erro: Todos os campos da vaga devem ser preenchidos.")
else:
    # Criar uma instância de Job com informações da vaga
    job = Job(
        id=str(uuid.uuid4()),  # Gera um ID único para a vaga
        name=name,
        main_activities=activities,
        prerequisites=prerequisites,
        differentials=differentials,
    )

    # Inserir a vaga no banco de dados com tratamento de erro
    try:
        # Tente inserir a vaga no banco de dados
        database.jobs.insert(job.model_dump())
        print(f"Vaga '{name}' inserida com sucesso no banco de dados.")
    except Exception as e:
        print(f"Erro ao inserir a vaga no banco de dados: {e}")
