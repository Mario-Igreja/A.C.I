from sqlalchemy import create_engine, Column, String, Text, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from typing import List, Optional

Base = declarative_base()

# Modelo para a tabela de Vagas (Job)
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(String, primary_key=True)  # ID da vaga
    name = Column(String, nullable=False)  # Nome da vaga
    main_activities = Column(Text, nullable=False)  # Atividades principais
    prerequisites = Column(Text, nullable=False)  # Pré-requisitos
    differentials = Column(Text, nullable=True)  # Diferenciais
    resums = relationship('Resum', back_populates='job')  # Relação com Resum

# Modelo para a tabela de Resumos (Resum)
class Resum(Base):
    __tablename__ = 'resums'
    id = Column(String, primary_key=True)  # ID do resumo
    job_id = Column(String, ForeignKey('jobs.id'), nullable=False)  # ID da vaga associada
    content = Column(Text, nullable=False)  # Conteúdo do resumo
    opinion = Column(Text, nullable=True)  # Opinião sobre o resumo
    file = Column(String, nullable=True)  # Nome do arquivo do resumo
    job = relationship('Job', back_populates='resums')  # Relação com Job

# Modelo para a tabela de Análises (Analysis)
class Analysis(Base):
    __tablename__ = 'analysis'
    id = Column(String, primary_key=True)  # ID da análise
    job_id = Column(String, ForeignKey('jobs.id'), nullable=False)  # ID da vaga associada
    resum_id = Column(String, ForeignKey('resums.id'), nullable=False)  # ID do resumo associado
    name = Column(String, nullable=False)  # Nome da análise
    skills = Column(Text, nullable=False)  # Habilidades como texto
    education = Column(Text, nullable=False)  # Educação como texto
    languages = Column(Text, nullable=False)  # Idiomas como texto
    score = Column(Float, nullable=False)  # Pontuação da análise

# Modelo para a tabela de Arquivos (File)
class File(Base):
    __tablename__ = 'files'
    file_id = Column(String, primary_key=True)  # ID do arquivo
    job_id = Column(String, ForeignKey('jobs.id'), nullable=False)  # ID da vaga associada
    # Você pode adicionar outros atributos necessários para o arquivo aqui
    job = relationship('Job')  # Relação com Job

# Classe para inicializar e manipular a base de dados
class AnalizadorDatabase:
    def __init__(self, db_url='mysql+mysqlconnector://user:password@localhost:3306/cv_analizador'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_job_by_name(self, name: str) -> Optional[Job]:
        with self.Session() as session:
            return session.query(Job).filter(Job.name == name).first()

    def get_resum_by_id(self, id: str) -> Optional[Resum]:
        with self.Session() as session:
            return session.query(Resum).filter(Resum.id == id).first()

    def get_analysis_by_job_id(self, job_id: str) -> List[Analysis]:
        with self.Session() as session:
            return session.query(Analysis).filter(Analysis.job_id == job_id).all()

    def get_resums_by_job_id(self, job_id: str) -> List[Resum]:
        with self.Session() as session:
            return session.query(Resum).filter(Resum.job_id == job_id).all()

    def delete_all_resums_by_job_id(self, job_id: str) -> None:
        with self.Session() as session:
            session.query(Resum).filter(Resum.job_id == job_id).delete()
            session.commit()

    def delete_all_analysis_by_job_id(self, job_id: str) -> None:
        with self.Session() as session:
            session.query(Analysis).filter(Analysis.job_id == job_id).delete()
            session.commit()

    def delete_all_files_by_job_id(self, job_id: str) -> None:
        with self.Session() as session:
            session.query(File).filter(File.job_id == job_id).delete()
            session.commit()
