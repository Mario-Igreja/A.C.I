import os
import streamlit as st
import pandas as pd
import altair as alt
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from database import AnalizadorDatabase

# Inicializa a base de dados
database = AnalizadorDatabase()

# Configura a página do Streamlit com layout largo e título "Recrutador"
st.set_page_config(layout="wide", page_title="Recrutador", page_icon=":brain:")

# Função para deletar arquivos dos currículos
def delete_files_resum(resums):
    for resum in resums:
        path = resum.get('file')
        if os.path.isfile(path):
            try:
                os.remove(path)
                st.success(f"Arquivo {path} excluído com sucesso.")
            except Exception as e:
                st.warning(f"Erro ao excluir o arquivo {path}: {e}")

# Função para exibir gráfico de pontuação dos candidatos com cores diferentes
def exibir_grafico(df):
    st.subheader('Classificação dos Candidatos')
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Nome", sort="-y"),
        y=alt.Y("Score"),
        color=alt.Color("Nome", scale=alt.Scale(scheme="tableau10"))  # Define uma paleta de cores
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

# Função para configurar e exibir a tabela interativa dos candidatos
def exibir_tabela_interativa(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_column("Score", header_name="Score", sort="desc")
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gb.build()
    
    return AgGrid(
        df, gridOptions=grid_options, enable_enterprise_modules=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED, theme='streamlit'
    )

# Função para verificar se a vaga e os dados existem
def carregar_vaga_analises(job_name):
    try:
        job = database.get_job_by_name(job_name)
        if job:
            data = database.get_analysis_by_job_id(job.get('id'))
            return job, data
        else:
            st.warning(f"Vaga {job_name} não encontrada.")
            return None, None
    except Exception as e:
        st.error(f"Erro ao carregar dados da vaga {job_name}: {e}")
        return None, None

# Cria um menu de seleção para escolher uma vaga disponível na base de dados
try:
    jobs = [job.get('name') for job in database.jobs.all()]
    if jobs:
        option = st.selectbox("Escolha sua vaga:", jobs, index=0)
    else:
        st.warning("Nenhuma vaga disponível no banco de dados.")
        option = None
except Exception as e:
    st.error(f"Erro ao carregar vagas: {e}")
    option = None

# Inicializa a variável `data`
data = None

# Verifica se uma vaga foi selecionada
if option:
    job, data = carregar_vaga_analises(option)
    
    # Se os dados da vaga e análises existirem, exibe as informações
    if job and data:
        try:
            # Cria o DataFrame com as análises
            df = pd.DataFrame(data, columns=[
                'name', 'education', 'skills', 'languages', 'score', 'resum_id', 'id'
            ])
            df.rename(columns={
                'name': 'Nome', 'education': 'Educação', 'skills': 'Habilidades',
                'languages': 'Idiomas', 'score': 'Score', 'resum_id': 'Resum ID', 'id': 'ID'
            }, inplace=True)

            # Exibe o gráfico de pontuações dos candidatos
            exibir_grafico(df)

            # Exibe a tabela interativa dos candidatos
            response = exibir_tabela_interativa(df)

            # Obtém os candidatos selecionados na tabela
            selected_candidates = response.get('selected_rows', [])
            candidates_df = pd.DataFrame(selected_candidates)

            # Obtém os currículos relacionados à vaga
            resums = database.get_resums_by_job_id(job.get('id'))

            # Botão para limpar as análises e deletar os currículos
            if st.button('Limpar Análise'):
                database.delete_all_resums_by_job_id(job.get('id'))
                database.delete_all_analysis_by_job_id(job.get('id'))
                database.delete_all_files_by_job_id(job.get('id'))
                delete_files_resum(resums)
                st.success("Análises e currículos excluídos com sucesso.")
                st.experimental_rerun()

            # Exibe os currículos dos candidatos selecionados
            if not candidates_df.empty:
                cols = st.columns(len(candidates_df))
                for idx, row in enumerate(candidates_df.iterrows()):
                    with cols[idx]:
                        resum_data = database.get_resum_by_id(row[1]['Resum ID'])
                        if resum_data:
                            st.markdown(resum_data.get('content'))
                            st.markdown(resum_data.get('opnion'))

                            with open(resum_data.get('file'), "rb") as pdf_file:
                                pdf_data = pdf_file.read()
                                st.download_button(
                                    label=f"Download Currículo {row[1]['Nome']}",
                                    data=pdf_data,
                                    file_name=f"{row[1]['Nome']}.pdf",
                                    mime="application/pdf"
                                )
        except Exception as e:
            st.error(f"Erro ao processar as análises da vaga {option}: {e}")
    else:
        st.warning("Nenhuma análise encontrada para esta vaga.")
