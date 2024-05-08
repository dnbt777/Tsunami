import json
from Tsunami.ProjectConfig import ProjectConfig
from Tsunami.Metrics.CostTracker import CostTracker
from Tsunami.DataAnalysis.DataAnalysisJob import DataAnalysisJob
from Tsunami.DocScraper.DataRequest import DataRequestJobs

class ProjectLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.data = self.load_project_from_config()

    def load_project_from_config(self):
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def get_project_config(self):
        config_data = self.data['project_config']
        cost_tracker = CostTracker() if config_data.get('cost_tracker', False) else None
        return ProjectConfig(
            workspace=config_data['workspace'],
            cost_tracker=cost_tracker,
            ratelimit_delay_seconds=config_data['ratelimit_delay_seconds'],
            continue_analysis=config_data['continue_analysis']
        )

    def get_data_request_jobs(self):
        return DataRequestJobs(self.data['data_requests'])

    def get_analysis_requests(self):
        return DataAnalysisJob(self.data['analysis_requests'])