from Tsunami.DocScraper.DataRequest import DataRequestJobs
from Tsunami.DocScraper.DocScraperManager import DocScraperManager

class Downloader:
    def __init__(self, project_config, datarequestjobs):
        self.project_config = project_config
        self.datarequestjobs = datarequestjobs

    def execute(self):
        docscraper = DocScraperManager(self.project_config)
        docscraper.execute_jobs(self.datarequestjobs)