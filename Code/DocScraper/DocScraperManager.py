
#
from Code.DocScraper.Scrapers.GPSScraper import GPSScraper
from Code.DocScraper.Scrapers.YTScraper import YTScraper
from Code.DocScraper.Scrapers.SemanticArxivScraper import SemanticArxivScraper
from Code.DocScraper.Scrapers.DepthCrawlerScraper import DepthCrawlerScraper
from Code.DocScraper.Scrapers.GitHubScraper import GitHubScraper


from Code.DocScraper.DataRequest import DataRequestJobs, DataRequestJob
from Code.ProjectConfig import ProjectConfig
import os


# Possible additions
# scrape top n youtube videos based on query

# A manager of doc scrapers
# Manages each type of doc scraper. Routes jobs to the appropriate scraper.
class DocScraperManager():
    def __init__(self, project_config : ProjectConfig):
        self.data_download_directory = project_config.data_download_directory
        os.makedirs(self.data_download_directory, exist_ok=True)
        self.project_config = project_config



    # Execute all jobs in a DataRequestJobs object
    def execute_jobs(self, datarequestjobs : DataRequestJobs):
        for datarequestjob in datarequestjobs.jobs:
            self.execute_job(datarequestjob)



    # Execute single DataRequestJob
    # Sends job to appropriate scraper
    def execute_job(self, datarequestjob : DataRequestJob):
        scraper = {
            "gps"       : GPSScraper,
            "youtube"   : YTScraper,
            "arxiv"     : SemanticArxivScraper,
            "spotify"   : None,
            "webcrawler": DepthCrawlerScraper,
            "github" : GitHubScraper,
        }[datarequestjob.source]
        # Set params in datarequestjob
        datarequestjob.ratelimit_delay_seconds = self.project_config.ratelimit_delay_seconds # TODO make this clean["ratelimit_delay_seconds"]
        scraper.execute_job(datarequestjob, self.data_download_directory)


    





