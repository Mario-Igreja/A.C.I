from tinydb import TinyDB, Query

class AnalizadorDatabase(TinyDB):
    def __init__(self, file_path='db.json') -> None:
        super().__init__(file_path)
        self.jobs = self.table('jobs')
        self.resums = self.table('resums')
        self.analysis = self.table('analysis')
        self.files = self.table('files')

    def get_job_by_name(self, name):
        job = Query()
        result = self.jobs.search(job.name == name)
        return result[0] if result else None
    
    def get_resum_by_id(self, id):
        resum = Query()
        result = self.resums.search(resum.id == id)
        return result[0] if result else None

    def get_analysis_by_job_id(self, job_id):
        analysis = Query()
        result = self.analysis.search(analysis.job_id == job_id)
        return result

    def get_resums_by_job_id(self, job_id):
        resum = Query()
        result = self.resums.search(resum.job_id == job_id)
        return result

    def delete_all_resums_by_job_id(self, job_id):
        resum = Query()
        self.resums.remove(resum.job_id == job_id)

    def delete_all_analysis_by_job_id(self, job_id):
        analysis = Query()
        self.analysis.remove(analysis.job_id == job_id)

    def delete_all_files_by_job_id(self, job_id):
        file = Query()
        self.files.remove(file.job_id == job_id)

    def delete_job(self, job_id):
        job = Query()
        job_to_delete = self.jobs.search(job.id == job_id)
        
        if job_to_delete:
            self.delete_all_resums_by_job_id(job_id)
            self.delete_all_analysis_by_job_id(job_id)
            self.delete_all_files_by_job_id(job_id)
            self.jobs.remove(job.id == job_id)
            print(f"Vaga com ID {job_id} deletada com sucesso!")
        else:
            print(f"Nenhuma vaga encontrada com o ID {job_id}.")

    def edit_job(self, job_id, new_data):
        job = Query()
        job_to_edit = self.jobs.search(job.id == job_id)
        
        if job_to_edit:
            self.jobs.update(new_data, job.id == job_id)
            print(f"Vaga com ID {job_id} atualizada com sucesso!")
        else:
            print(f"Nenhuma vaga encontrada com o ID {job_id}.")
