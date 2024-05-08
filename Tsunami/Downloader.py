class Downloader:
    def __init__(self, project_config, datarequestjobs_list_json):
        self.project_config = project_config
        self.datarequestjobs_list_json = datarequestjobs_list_json

    def execute(self):
        datarequestjobs = DataRequestJobs(self.datarequestjobs_list_json)
        docscraper = DocScraperManager(self.project_config)
        docscraper.execute_jobs(datarequestjobs)