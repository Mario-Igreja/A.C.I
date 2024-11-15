def remove_vaga():
    # Importa dentro da função para evitar problemas de importação circular
    from database import AnalizadorDatabase

    # Criar uma instância do banco de dados
    database = AnalizadorDatabase()

    # Lista de vagas a serem removidas
    job_names_to_remove = [
        "Vaga de Gestor Comercial de B2B",
        "Engenheiro de Projetos de Infraestrutura",
        "Advogado Especialista em Direito Trabalhista"
    ]

    # Remover as vagas pelo nome
    for job_name in job_names_to_remove:
        # Chama a função delete_job_by_name para excluir a vaga
        database.delete_job_by_name(job_name)
        print(f"Vaga '{job_name}' removida com sucesso.")

    # Caso queira remover por ID, você pode usar a mesma lógica, mas passando os IDs específicos:
    # job_ids_to_remove = ["id_da_vaga_comercial", "id_da_vaga_engenharia", "id_da_vaga_juridica"]
    # for job_id in job_ids_to_remove:
    #     database.delete_job_by_id(job_id)
    #     print(f"Vaga com ID '{job_id}' removida com sucesso.")

    # Exemplo de pegar a análise por ID de vaga
    job_id = "id_da_vaga_comercial"  # Substitua com o ID real
    analysis_results = database.get_analysis_by_job_id(job_id)
    
    if analysis_results:
        print(f"Análises encontradas: {analysis_results}")
    else:
        print(f"Nenhuma análise encontrada para a vaga de ID '{job_id}'.")

# Chame a função para executar
remove_vaga()
