from Tsunami.DataAnalysis.RAGManager import RAGManager
from Tsunami.DataAnalysis.RAGCreationJob import RAGCreationJob

class RAGGenerator:
    def __init__(self, project_config, rag_generation_job):
        self.project_config = project_config
        self.rag_generation_job = rag_generation_job

    def execute(self):
        rag_creation_manager = RAGManager(self.project_config)
        rag_creation_manager.execute_job(self.rag_generation_job)