# A.C.I



---

## SUMÁRIO

- [Descrição](#descrição)
- [Problemática](#problemática)
- [Hipótese](#hipótese)
- [Objetivos](#objetivos)
  - [Geral](#geral)
  - [Específicos](#específicos)
- [Sistemas de Informação Geográficos](#sistemas-de-informação-geográficos)
- [Especificações Técnicas](#especificações-técnicas)
  - [O Web site (Front-End)](#o-web-site-front-end)
  - [O servidor Web (Back-End)](#o-servidor-web-back-end)
  - [Base de dados](#base-de-dados)

## Descrição

O **Analisador de Currículos** é uma aplicação que permite realizar a análise automatizada de currículos em lote, utilizando inteligência artificial para comparar currículos com base em uma vaga específica. A aplicação também gera relatórios descritivos e pontua os currículos conforme a adequação dos candidatos à vaga.

Utilizando tecnologias como Python para a lógica de backend, **Streamlit** para o frontend e a **API Groq (Llama 3.1)** para realizar o processamento e pontuação dos currículos, o projeto permite que empresas otimizem o processo de seleção de candidatos.

## Problemática

A seleção de candidatos para vagas de emprego, especialmente em grandes volumes, é um processo longo e suscetível a erros humanos. A avaliação manual de currículos pode não ser consistente e consome muito tempo, dificultando o encontro dos melhores candidatos de forma rápida e eficiente.

## Hipótese

Ao automatizar o processo de análise de currículos com ferramentas de inteligência artificial, é possível reduzir significativamente o tempo necessário para avaliar e classificar candidatos, além de melhorar a precisão e consistência na seleção.

## Objetivos

### Geral
O objetivo principal deste projeto é desenvolver uma ferramenta que permita a análise rápida, precisa e objetiva de currículos, otimizando o processo de contratação para empresas.

### Específicos
- Implementar um sistema de upload em lote para processar múltiplos currículos ao mesmo tempo.
- Desenvolver uma interface amigável para a comparação de currículos.
- Utilizar IA para fornecer análises críticas e gerar uma pontuação de adequação com base em uma vaga específica.
- Gerar relatórios descritivos que possam ser utilizados pelos recrutadores durante a seleção.

## Sistemas de Informação Geográficos

Nesta aplicação, não há diretamente o uso de um Sistema de Informação Geográfico (SIG), mas o conceito pode ser estendido para análise de distribuição geográfica de candidatos em futuras versões.

## Especificações Técnicas

### O Web site (Front-End)
A interface é construída com **Streamlit**, uma biblioteca Python que facilita a criação de dashboards interativos e fáceis de usar. O usuário pode fazer o upload de documentos, visualizar análises e comparar resultados diretamente na interface web.

### O servidor Web (Back-End)
O backend é composto por um **Servidor Streamlit** que interage com diversos serviços, como o serviço de autenticação, banco de dados, serviço de cache e o serviço de análise de currículos. A API Groq é chamada para realizar o resumo e a análise dos currículos.

#### Tecnologias:
- **Python**: Utilizado para lógica de negócio e integração com APIs.
- **Poetry**: Para gerenciar dependências do projeto.
- **Groq API**: Utilizada para processar, resumir e pontuar os currículos.

### Base de dados
A aplicação utiliza um banco de dados para armazenar informações de currículos, vagas e resultados de análises. O banco de dados interage diretamente com o módulo de análise, facilitando o armazenamento e recuperação de dados conforme necessário.

## Instalação e Execução

### Pré-requisitos
- **Python 3.10 ou superior**: Necessário para rodar a aplicação.
- **Poetry**: Ferramenta de gerenciamento de dependências e ambientes virtuais, deve estar instalada globalmente.



 **Integrantes do Grupo:**

> **20221425** – Alfredo Bumba

> **20220812** – Leonardo Alves

> **20220672** - Mário Igreja

