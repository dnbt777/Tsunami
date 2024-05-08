class Analyzer:
    def __init__(self, project_config, analysisrequestjobs_json):
        self.project_config = project_config
        self.analysisrequestjobs_json = analysisrequestjobs_json

    def execute(self):
        data_analysis_manager = DataAnalysisManager(self.project_config)
        data_analysis_job = DataAnalysisJob(self.analysisrequestjobs_json)
        data_analysis_manager.execute_job(data_analysis_job)