from Tsunami.DataAnalysis.DataAnalysisManager import DataAnalysisManager
from Tsunami.DataAnalysis.DataAnalysisJob import DataAnalysisJob

class Analyzer:
    def __init__(self, project_config, analysisrequestjob):
        self.project_config = project_config
        self.analysisrequestjob = analysisrequestjob

    def execute(self):
        data_analysis_manager = DataAnalysisManager(self.project_config)
        data_analysis_manager.execute_job(self.analysisrequestjob)