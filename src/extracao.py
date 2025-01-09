# extracao.py
import re

def extract_experience_from_cv(cv_text):
    # Exemplo de extração de experiência a partir de texto de currículo
    experience = re.findall(r"\d+ anos de experiência", cv_text)
    return experience[0] if experience else "0 anos"

def extract_skills_from_cv(cv_text):
    # Exemplo de extração de habilidades a partir de texto de currículo
    skills = re.findall(r"\b\w+\b", cv_text)  # Extração simples
    return skills

def extract_education_from_cv(cv_text):
    # Exemplo de extração de educação a partir de texto de currículo
    education = re.search(r"Bacharelado em (\w+)", cv_text)
    return education.group(1) if education else ""

def extract_experience_from_job(job_description):
    # Extração da experiência necessária da descrição da vaga
    experience = re.findall(r"Experiência mínima de (\d+) anos", job_description)
    return int(experience[0]) if experience else 0

def extract_skills_from_job(job_description):
    # Extração das habilidades necessárias da descrição da vaga
    skills = re.findall(r"Habilidades necessárias: ([\w, ]+)", job_description)
    return skills[0].split(", ") if skills else []

def extract_education_from_job(job_description):
    # Extração do grau educacional da descrição da vaga
    education = re.search(r"Grau educacional: (\w+)", job_description)
    return education.group(1) if education else ""
