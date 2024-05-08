"""
job_ = {
    "source" : "youtube",
    "queries" : [ # TODO
        "cancer treatment 101 tutorial",
        "etc",
    ],
    "links" : [
        "https://youtube.com/v?ID=123012083190a", # video
        "https://playlist for yt", #playlist of videos
        "etc",
    ],
}
jobs_ = [job_, job_] # example
"""


class DataRequestJob():
    def __init__(self, **datarequest_json):
        # Set data source vars
        self.source = datarequest_json.get("source") # .get does not error out if not found 
        self.queries = datarequest_json.get("queries")
        self.links = datarequest_json.get("links")
        self.document_analysis_limit_per_query = datarequest_json.get("document_analysis_limit_per_query")
        self.special_links = datarequest_json.get("special_links")
        self.document_analysis_limit_per_playlist = datarequest_json.get("document_analysis_limit_per_playlist")
        self.file_types_to_ignore = datarequest_json.get("file_types_to_ignore")
                
        # Cover any other misc kwargs
        if datarequest_json:
            for key, value in datarequest_json.items():
                setattr(self, key, value)
    


# A request for data to be scraped
# Gets sent to DocScraper/DataScraper for scraping
class DataRequestJobs():
    def __init__(self, jobs_list_json):
        self.jobs = self.make_jobs(jobs_list_json)


    def make_jobs(self, datarequest_jobs_list_json):
        datarequestjobs = []
        for datarequest_job_json in datarequest_jobs_list_json:
            datarequestjob = DataRequestJob(**datarequest_job_json)
            datarequestjobs.append(datarequestjob)
        return datarequestjobs
            